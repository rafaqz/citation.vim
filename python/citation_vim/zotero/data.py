# -*- coding:utf-8 -*-

import sqlite3
import os
import os.path
import sys
import shutil
import sys
import time
from citation_vim.utils import compat_str, is_current
from citation_vim.zotero.item import zoteroItem
from citation_vim.utils import raiseError

class zoteroData(object):

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
                or fields.fieldName = "publicationTitle"
                or fields.fieldName = "volume"
                or fields.fieldName = "publication"
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

    tag_query = u"""
        SELECT items.itemID, tags.name
        FROM items, tags, itemTags
        WHERE
            items.itemID = itemTags.itemID
            and tags.tagID = itemTags.tagID
        """
    def __init__(self, context):
        self.context = context
        # Set paths
        self.storage_path = os.path.join(context.zotero_path, u"storage")
        self.attachment_base_path = context.zotero_attachment_path
        self.zotero_database = os.path.join(context.zotero_path, u"zotero.sqlite")
        self.database_copy = os.path.join(context.cache_path, u"zotero.sqlite")
        # These extensions are recognized as openable file attachments
        self.attachment_extensions = u".pdf", u".ps", u".epub"
        self.index = {}
        self.collection_index = []
        self.ignored = []
        self.fulltext_matches = []
        self.fulltext = False
        # Copy the zotero database
        if not is_current(self.zotero_database, self.database_copy):
            shutil.copyfile(self.zotero_database, self.database_copy)
        self.conn = sqlite3.connect(self.database_copy)
        self.cur = self.conn.cursor()

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

    def load(self):
        """
        Returns filtered, complete items
        """
        if not self.exists(): 
            return []
        self.ignore_deleted()
        if len(self.context.searchkeys) > 0:
            self.fulltext = True
            self.get_fulltext_matches()
        self.filter_items()
        self.get_info()
        self.get_authors()
        self.get_collections()
        self.get_tags()
        self.get_notes()
        self.get_attachments()
        return self.index.items()

    def ignore_deleted(self):
        """
        Populate self.ignored with deleted ids.
        """
        self.cur.execute(self.deleted_query)
        for item in self.cur.fetchall():
            self.ignored.append(item[0])

    def get_fulltext_matches(self):
        """
        Populate self.fulltext_matches with ids.
        Uses awfull string query building.
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
            searchkey = "jamaica" #self.context.searchkeys[i].lower()
            _froms += fulltext_from.replace('#', str(i))
            wheres += fulltext_where.replace('#', str(i)).format(searchkey)
        query = fulltext_select + _froms + '\nWHERE\n' + wheres
        self.cur.execute(query)
        for item in self.cur.fetchall():
            item_id = item[0]
            if not item_id in self.ignored: 
                self.fulltext_matches.append(item_id)

    def filter_items(self):
        """
        Populates self.index with new items, filtering out 
        ignored types and unmatched searches
        """
        self.cur.execute(self.type_query)
        for item in self.cur.fetchall():
            item_id = item[0]
            item_type = item[1]
            if item_id in self.ignored:
                continue
            if item_type in ["note","attachment"]:
                self.ignored.append(item_id)
                continue
            if self.fulltext and not item_id in self.fulltext_matches:
                continue

            self.index[item_id] = zoteroItem(item_id)
            self.index[item_id].type = item_type

    def get_info(self):
        """
        Adds flat data to self.index Items
        """
        field_mapping = {
            u"date": 'date',
            u"publicationTitle": 'publication',
            u"publisher": 'publisher',
            u"language": 'language',
            u"DOI": 'doi',
            u"ISBN": 'isbn',
            u"volume": 'volume',
            u"issue": 'issue',
            u"pages": 'pages',
            u"url": 'url',
            u"title": 'title',
            u"abstractNote": 'abstract'
        }

        self.cur.execute(self.info_query)
        for item in self.cur.fetchall():
            item_id = item[0]
            if item_id in self.index:
                key = item[3]
                self.index[item_id].key = key
                item_name = item[1]
                item_value = item[2]
                if item_name in field_mapping:
                    attribute = field_mapping[item_name]
                    setattr(self.index[item_id], attribute, item_value)


    def get_authors(self):
        """
        Adds author arrays to self.index Items
        """
        if self.context.zotero_version == 5:
            self.cur.execute(self.author_query_v5)
        else:
            self.cur.execute(self.author_query_v4)
        for item in self.cur.fetchall():
            item_id = item[0]
            if item_id in self.index:
                item_lastname = item[1]
                item_firstname = item[2]
                self.index[item_id].authors.append([item_lastname ,item_firstname])

    def get_collections(self):
        """
        Adds collection arrays to self.index Items
        """
        self.cur.execute(self.collection_query)
        for item in self.cur.fetchall():
            item_id = item[0]
            if item_id in self.index:
                item_collection = item[1]
                self.index[item_id].collections.append(item_collection)

    def get_tags(self):
        """
        Adds tags arrays to self.index Items
        """
        self.cur.execute(self.tag_query)
        for item in self.cur.fetchall():
            item_id = item[0]
            if item_id in self.index:
                item_tag = item[1]
                self.index[item_id].tags.append(item_tag)
                
    def get_notes(self):
        """
        Adds notes arrays to self.index Items
        """
        self.cur.execute(self.note_query)
        for item in self.cur.fetchall():
            item_id = item[0]
            if item_id in self.index:
                item_note = item[1]
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
            attachment_path = self.parse_attachment(item)
            item_id = item[0]
            if self.attachment_has_right_extension(attachment_path):
                self.index[item_id].fulltext.append(attachment_path)
        self.cur.close()

    def parse_attachment(self, item):
        item_id = item[0]
        if item_id in self.index:
            if item[1] != None:
                attachment_string = item[1]
                attachment_id = item[2]
                if attachment_string[:8] == u"storage:":
                    return self.format_storage_path(attachment_string, attachment_id)
                if attachment_string[:12] == u"attachments:":
                    return self.format_attachment_path(attachment_string)
                return self.format_plain_path(attachment_string)

    def format_storage_path(self, attachment_string, attachment_id):
        attachment_path = attachment_string[8:]
        if not self.attachment_has_right_extension(attachment_path):
            return ""

        self.cur.execute(u"select items.key from items where itemID = %d" \
           % attachment_id)
        key = self.cur.fetchone()[0]
        return os.path.join(self.storage_path, key, attachment_path)

    def format_attachment_path(self, attachment_string):
        attachment_path = attachment_string[12:]
        return os.path.join(self.attachment_base_path, attachment_path)

    def format_plain_path(self, attachment_string):
        return attachment_string

    def attachment_has_right_extension(self, path):
        return path and path[-4:].lower() in self.attachment_extensions

