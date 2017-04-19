# -*- coding:utf-8 -*-

import sqlite3
import os
import os.path
import sys
import shutil
import sys
import time
from citation_vim.utils import compat_str, is_current
from citation_vim.zotero.item import ZoteroItem
from citation_vim.utils import raiseError

class ZoteroData(object):

    """
    Provides access to the zotero database.
    Modified from LibZotero in gnotero.
    """

    deleted_query = u"SELECT itemID FROM deletedItems"

    type_query = u"""
        SELECT items.itemID, itemTypes.typeName
        FROM items, itemTypes
        WHERE
            items.itemTypeID = itemTypes.itemTypeID
        """

    info_query = u"""
        SELECT items.itemID, fields.fieldName, itemDataValues.value, items.key
        FROM items, itemData, fields, itemDataValues
        WHERE
            items.itemID = itemData.itemID
            and itemData.fieldID = fields.fieldID
            and itemData.valueID = itemDataValues.valueID
            and (fields.fieldName = "date"
                or fields.fieldName = "abstractNote"
                or fields.fieldName = "volume"
                or fields.fieldName = "publisher"
                or fields.fieldName = "publicationTitle"
                or fields.fieldName = "pages"
                or fields.fieldName = "url"
                or fields.fieldName = "DOI"
                or fields.fieldName = "ISBN"
                or fields.fieldName = "language"
                or fields.fieldName = "issue"
                or fields.fieldName = "title")
        """

    attachment_query_v4 = u"""
        SELECT items.itemID, itemAttachments.path, itemAttachments.itemID
        FROM items, itemAttachments
        WHERE items.itemID = itemAttachments.sourceItemID
        """

    attachment_query_v5 = u"""
        SELECT items.itemID, itemAttachments.path, itemAttachments.itemID
        FROM items, itemAttachments
        WHERE items.itemID = itemAttachments.parentItemID
        """

    author_query_v4 = u"""
        SELECT items.itemID, creatorData.lastName, creatorData.firstName
        FROM items, itemCreators, creators, creatorData, creatorTypes
        WHERE
            items.itemID = itemCreators.itemID
            and itemCreators.creatorID = creators.creatorID
            and creators.creatorDataID = creatorData.creatorDataID
            and itemCreators.creatorTypeID = creatorTypes.creatorTypeID
            and creatorTypes.creatorType != "editor"
        ORDER by itemCreators.ORDERIndex
        """

    author_query_v5 = u"""
        SELECT items.itemID, creators.lastName, creators.firstName
        FROM items, itemCreators, creators, creatorTypes
        WHERE
            items.itemID = itemCreators.itemID
            and itemCreators.creatorID = creators.creatorID
            and creators.creatorID = creators.creatorID
            and itemCreators.creatorTypeID = creatorTypes.creatorTypeID
            and creatorTypes.creatorType != "editor"
        ORDER by itemCreators.ORDERIndex
        """
    collection_query = u"""
        SELECT items.itemID, collections.collectionName
        FROM items, collections, collectionItems
        WHERE
            items.itemID = collectionItems.itemID
            and collections.collectionID = collectionItems.collectionID
        ORDER by collections.collectionName != "To Read",
            collections.collectionName
        """

    note_query = u"""
        SELECT items.itemID, itemNotes.note
        FROM items, itemNotes
        WHERE
            items.itemID = itemNotes.itemID
        """

    note_query_v5 = u"""
        SELECT itemNotes.parentItemID, itemNotes.note
        FROM itemNotes
        WHERE
            itemNotes.parentItemID IS NOT NULL;
        """

    tag_query = u"""
        SELECT items.itemID, tags.name
        FROM items, tags, itemTags
        WHERE
            items.itemID = itemTags.itemID
            and tags.tagID = itemTags.tagID
        """

    attachment_extensions = u".pdf", u".ps", u".epub"


    def __init__(self, context):
        self.context = context
        self.set_paths()
        self.init_database()

    def set_paths(self):
        self.storage_path = os.path.join(self.context.zotero_path, u"storage")
        self.attachment_base_path = self.context.zotero_attachment_path
        self.zotero_database = os.path.join(self.context.zotero_path, u"zotero.sqlite")
        self.database_copy = os.path.join(self.context.cache_path, u"zotero.sqlite")

    def init_database(self):
        # Copy the zotero database
        if not is_current(self.zotero_database, self.database_copy):
            shutil.copyfile(self.zotero_database, self.database_copy)
        self.conn = sqlite3.connect(self.database_copy)
        self.cur = self.conn.cursor()


    def load(self):
        """
        Returns filtered, complete items
        """
        if not self.exists(): 
            return []
        self.filter_items()
        self.get_item_detail()
        return self.index.items()

    def exists(self):
        """
        Returns: True/False for database existance.
        """
        try:
            stats = os.stat(self.zotero_database)
        except Exception as e:
            raiseError(u"citation_vim.zotero.data.exists(): %s" % e)
            return False
        return True


    def filter_items(self):
        """
        Populates self.index with new items, filtering out 
        ignored types and unmatched searches
        """
        self.ignore_deleted()
        self.do_fulltext_search()
        self.index = {}
        self.cur.execute(self.type_query)
        for [item_id, item_type] in self.cur.fetchall():
            if item_id in self.ignored:
                continue
            if item_type in ["note","attachment"]:
                self.ignored.append(item_id)
                continue
            if self.fulltext and not item_id in self.fulltext_matches:
                continue
            self.index[item_id] = ZoteroItem(item_id)
            self.index[item_id].type = item_type

    def get_item_detail(self):
        self.get_info()
        self.get_authors()
        self.get_collections()
        self.get_tags()
        self.get_notes()
        self.get_attachments()

    def ignore_deleted(self):
        """
        Populate self.ignored with deleted ids.
        """
        self.deleted = []
        self.cur.execute(self.deleted_query)
        for item in self.cur.fetchall():
            item_id = item[0]
            self.deleted.append(item_id)
        # Using list() to ensure this is an actual duplicate .
        self.ignored = list(self.deleted)

    def do_fulltext_search(self):
        if len(self.context.searchkeys) > 0:
            self.fulltext = True
            self.get_fulltext_matches()
        else:
            self.fulltext = False

    def get_fulltext_matches(self):
        """
        Populate self.fulltext_matches with ids.
        """
        self.fulltext_matches = []
        query = self.build_fulltext_query()
        self.cur.execute(query)
        for [item_id] in self.cur.fetchall():
            if not item_id in self.ignored: 
                self.fulltext_matches.append(item_id)

    def build_fulltext_query(self):
        """
        Awful, awful string query building.
        """
        if self.context.zotero_version == 5:
            fulltext_select = u"""
                SELECT itemAttachments.parentItemID
                FROM itemAttachments"""
        else:
            fulltext_select = u"""
                SELECT itemAttachments.sourceItemID
                FROM itemAttachments"""
        fulltext_from = u", fulltextItemWords AS fIW#, fulltextWords AS fW#"
        fulltext_where = u"""itemAttachments.itemID = fIW#.itemID
            and fIW#.wordID = fW#.wordID
            and fW#.word = '{}'"""
        _froms = ''
        wheres = ''
        for i in range(len(self.context.searchkeys)):
            if i > 0: 
                wheres += '\nand '
            searchkey = self.context.searchkeys[i].lower()
            _froms += fulltext_from.replace('#', str(i))
            wheres += fulltext_where.replace('#', str(i)).format(searchkey)
        return fulltext_select + _froms + '\nWHERE\n' + wheres

    def get_info(self):
        """
        Adds flat data to self.index Items
        """
        self.cur.execute(self.info_query)
        for [item_id, item_name, item_value, key] in self.cur.fetchall():
            if item_id in self.index:
                self.index[item_id].key = key
                setattr(self.index[item_id], item_name, item_value)

    def get_authors(self):
        """
        Adds author arrays to self.index Items
        """
        if self.context.zotero_version == 5:
            self.cur.execute(self.author_query_v5)
        else:
            self.cur.execute(self.author_query_v4)
        for [item_id, item_lastname, item_firstname] in self.cur.fetchall():
            if item_id in self.index:
                self.index[item_id].authors.append([item_lastname ,item_firstname])

    def get_collections(self):
        """
        Adds collection arrays to self.index Items
        """
        self.cur.execute(self.collection_query)
        for [item_id, item_collection] in self.cur.fetchall():
            if item_id in self.index:
                self.index[item_id].collections.append(item_collection)

    def get_tags(self):
        """
        Adds tags arrays to self.index Items
        """
        self.cur.execute(self.tag_query)
        for [item_id, item_tag] in self.cur.fetchall():
            if item_id in self.index:
                self.index[item_id].tags.append(item_tag)
                
    def get_notes(self):
        """
        Adds notes arrays to self.index Items
        """
        if self.context.zotero_version == 5:
            self.cur.execute(self.note_query_v5)
        else:
            self.cur.execute(self.note_query)
        for [item_id, item_note] in self.cur.fetchall():
            if item_id in self.index:
                self.index[item_id].notes.append(item_note)

    def get_attachments(self):
        """
        Adds attachment arrays to self.index Items
        """
        if self.context.zotero_version == 5:
            self.cur.execute(self.attachment_query_v5)
        else:
            self.cur.execute(self.attachment_query_v4)
        for item in self.cur.fetchall():
            item_id = item[0]
            attachment_path = self.parse_attachment(item)
            if attachment_path and self.attachment_has_right_extension(attachment_path):
                self.index[item_id].attachments.append(attachment_path)
        self.cur.close()

    # Some parsing needs to be here because another call to the database is required
    def parse_attachment(self, item):
        item_id = item[0]
        if item_id in self.index:
            if item[1] == None:
                return None
            attachment_string = item[1]
            attachment_id = item[2]
            if attachment_id in self.deleted:
                return None
            if attachment_string[:8] == u"storage:":
                return self.get_storage_path(attachment_string[8:], attachment_id)
            if attachment_string[:12] == u"attachments:":
                return self.format_attachment_path(attachment_string[12:])
            return attachment_string

    def get_storage_path(self, attachment_path, attachment_id):
        if not self.attachment_has_right_extension(attachment_path):
            return ""
        key = self.get_storage_key(attachment_id)
        return os.path.join(self.storage_path, key, attachment_path)

    def get_storage_key(self, attachment_id):
        self.cur.execute(u"select items.key from items where itemID = %d" % attachment_id)
        return self.cur.fetchone()[0]

    def format_attachment_path(self, attachment_path):
        return os.path.join(self.attachment_base_path, attachment_path)

    def attachment_has_right_extension(self, path): 
        return path and os.path.splitext(path)[1] in self.attachment_extensions

