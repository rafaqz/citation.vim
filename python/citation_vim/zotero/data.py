#-*- coding:utf-8 -*-

import sqlite3
import os
import os.path
import sys
import shutil
import sys
import time

class zoteroData(object):

    """
    Provides access to the zotero database.
    Modified from LibZotero in gnotero.
    """

    attachment_query = u"""
        select items.itemID, itemAttachments.path, itemAttachments.itemID
        from items, itemAttachments
        where items.itemID = itemAttachments.sourceItemID
        """


    info_query = u"""
        select items.itemID, fields.fieldName, itemDataValues.value, items.key
        from items, itemData, fields, itemDataValues
        where
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

    author_query = u"""
        select items.itemID, creatorData.lastName, creatorData.firstName
        from items, itemCreators, creators, creatorData, creatorTypes
        where
            items.itemID = itemCreators.itemID
            and itemCreators.creatorID = creators.creatorID
            and creators.creatorDataID = creatorData.creatorDataID
            and itemCreators.creatorTypeID = creatorTypes.creatorTypeID
            and creatorTypes.creatorType != "editor"
        order by itemCreators.orderIndex
        """

    collection_query = u"""
        select items.itemID, collections.collectionName
        from items, collections, collectionItems
        where
            items.itemID = collectionItems.itemID
            and collections.collectionID = collectionItems.collectionID
        order by collections.collectionName != "To Read",
            collections.collectionName
        """

    type_query = u"""
        select items.itemID, itemTypes.typeName
        from items, itemTypes
        where
            items.itemTypeID = itemTypes.itemTypeID
        """

    tag_query = u"""
        select items.itemID, tags.name
        from items, tags, itemTags
        where
            items.itemID = itemTags.itemID
            and tags.tagID = itemTags.tagID
        """

    note_query = u"""
        select items.itemID, itemNotes.note
        from items, itemNotes
        where
            items.itemID = itemNotes.itemID
        """

    deleted_query = u"select itemID from deletedItems"

    def __init__(self, zotero_path, cache_path):

        """
        Intialize libzotero.
        Arguments:
        zotero_path       --    A string to the Zotero folder.

        Keyword arguments:
        """

        # Set paths
        self.storage_path = os.path.join(zotero_path, u"storage")
        self.zotero_database = os.path.join(zotero_path, u"zotero.sqlite")
        self.database_copy = os.path.join(cache_path, u".citation_vim.sqlite")
        # Remember search results so results speed up over time
        self.search_cache = {}
        # Check whether verbosity is turned on
        self.verbose = "-v" in sys.argv
        # These dates are treated as special and are not parsed into a year
        # representation
        self.special_dates = u"in press", u"submitted", u"in preparation", \
            u"unpublished"
        # These extensions are recognized as fulltext attachments
        self.attachment_ext = u".pdf", u".epub"

        self.index = {}
        self.collection_index = []
        self.tag_index = []
        self.note_index = []
        self.last_update = None


    def update(self, force=False):

        """
        Checks if the local copy of the zotero database is up to date. If not,
        the data is also indexed.

        Arguments:
        force       --    Indicates that the data should also be indexed, even
                        if the local copy is up to date. (default=False)
        """

        from citation_vim.zotero.item import zoteroItem

        try:
            stats = os.stat(self.zotero_database)
        except Exception as e:
            print(u"libzotero.update(): %s" % e)
            return False

        # Only update if necessary
        if force or self.last_update == None or stats[8] > self.last_update:
            t = time.time()
            self.last_update = stats[8]
            self.index = {}
            self.collection_index = []
            self.search_cache = {}
            # Copy the zotero database to the copy
            shutil.copyfile(self.zotero_database, self.database_copy)
            self.conn = sqlite3.connect(self.database_copy)
            self.cur = self.conn.cursor()
            # First create a list of deleted items, so we can ignore those later
            deleted = []
            ignored = []
            self.cur.execute(self.deleted_query)
            for item in self.cur.fetchall():
                deleted.append(item[0])

            # Retrieve type information and filter unwanted types.
            self.cur.execute(self.type_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                item_type = item[1]
                if item_id in deleted or item_type in ["note","attachment"]:
                    # Ignore deleted items, notes, and attachments
                    ignored.append(item_id)
                else:
                    if item_id not in self.index:
                        self.index[item_id] = zoteroItem(item_id)
                    self.index[item_id].type = item_type

            # Retrieve information about date, publication, volume, issue and
            # title
            self.cur.execute(self.info_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                key = item[3]
                if item_id not in ignored:
                    item_name = item[1]
                    # Parse date fields, because we only want a year or a #
                    # 'special' date
                    if item_name == u"date":
                        item_value = None
                        for sd in self.special_dates:
                            if sd in item[2].lower():
                                item_value = sd
                                break
                        # Dates can have months, days, and years, or just a
                        # year, and can be split by '-' and '/' characters.
                        if item_value == None:
                            # Detect whether the date should be split
                            if u'/' in item[2]:
                                split = u'/'
                            elif u'-' in item[3]:
                                split = u'-'
                            else:
                                split = None
                            # If not, just use the last four characters
                            if split == None:
                                item_value = item[2][-4:]
                            # Else take the first slice that is four characters
                            else:
                                l = item[2].split(split)
                                for i in l:
                                    if len(i) == 4:
                                        item_value = i
                                        break
                    else:
                        item_value = item[2]
                    if item_id not in self.index:
                        self.index[item_id] = zoteroItem(item_id)
                        self.index[item_id].key = key
                    if item_name == u"publicationTitle":
                        self.index[item_id].publication = str(item_value)
                    elif item_name == u"date":
                        self.index[item_id].date = item_value
                    elif item_name == u"publisher":
                        self.index[item_id].publisher = item_value
                    elif item_name == u"language":
                        self.index[item_id].language = item_value
                    elif item_name == u"DOI":
                        self.index[item_id].doi = item_value
                    elif item_name == u"ISBN":
                        self.index[item_id].isbn = item_value
                    elif item_name == u"volume":
                        self.index[item_id].volume = item_value
                    elif item_name == u"issue":
                        self.index[item_id].issue = item_value
                    elif item_name == u"pages":
                        self.index[item_id].pages = item_value
                    elif item_name == u"url":
                        self.index[item_id].url = item_value
                    elif item_name == u"title":
                        self.index[item_id].title = item_value
                    elif item_name == u"abstractNote":
                        self.index[item_id].abstract = item_value
            # Retrieve author information
            self.cur.execute(self.author_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in ignored:
                    item_lastname = item[1].title()
                    item_firstname = item[2].title()
                    if item_id not in self.index:
                        self.index[item_id] = zoteroItem(item_id)
                    self.index[item_id].authors.append([item_lastname ,item_firstname])
            # Retrieve collection information
            self.cur.execute(self.collection_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in ignored:
                    item_collection = item[1]
                    if item_id not in self.index:
                        self.index[item_id] = zoteroItem(item_id)
                    self.index[item_id].collections.append(item_collection)
                    if item_collection not in self.collection_index:
                        self.collection_index.append(item_collection)
            # Retrieve tag information
            self.cur.execute(self.tag_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in ignored:
                    item_tag = item[1]
                    if item_id not in self.index:
                        self.index[item_id] = zoteroItem(item_id)
                    self.index[item_id].tags.append(item_tag)
                    if item_tag not in self.tag_index:
                        self.tag_index.append(item_tag)
            # Retrieve note information
            self.cur.execute(self.note_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in ignored:
                    item_note = item[1]
                    if item_id not in self.index:
                        self.index[item_id] = zoteroItem(item_id)
                    self.index[item_id].notes.append(item_note)
                    if item_note not in self.note_index:
                        self.note_index.append(item_note)
            # Retrieve attachments
            self.cur.execute(self.attachment_query)
            for item in self.cur.fetchall():
                item_id = item[0]
                if item_id not in ignored:
                    if item[1] != None:
                        att = item[1]
                        # If the attachment is stored in the Zotero folder, it is preceded
                        # by "storage:"
                        if att[:8] == u"storage:":
                            item_attachment = att[8:]
                            # The item attachment appears to be encoded in
                            # latin-1 encoding, which we don't want, so recode.
                            item_attachment = item_attachment.encode(
                                'latin-1').decode('utf-8')
                            attachment_id = item[2]
                            if item_attachment[-4:].lower() in self.attachment_ext:
                                if item_id not in self.index:
                                    self.index[item_id] = zoteroItem(item_id)
                                self.cur.execute( \
                                    u"select items.key from items where itemID = %d" \
                                    % attachment_id)
                                key = self.cur.fetchone()[0]
                                self.index[item_id].fulltext.append(os.path.join( \
                                    self.storage_path, key, item_attachment))
                        # If the attachment is linked, it is simply the full
                        # path to the attachment
                        else:
                            self.index[item_id].fulltext.append(att)
            self.cur.close()
        return True

    def load(self):
        if not self.update():
            return []
        return self.index.items()

def valid_location(path):

    """
    Checks if a given path is a valid Zotero folder, i.e., if it it contains
    zotero.sqlite.

    Arguments:
    path      --    The path to check.

    Returns:
    True if path is a valid Zotero folder, False otherwise.
    """

    assert(isinstance(path, str))
    return os.path.exists(os.path.join(path, u"zotero.sqlite"))
