# -*- coding: utf-8 -*-

import os
import json
import shutil
import sqlite3
from citation_vim.zotero.data import valid_location, zoteroData
from citation_vim.item import Item

class zoteroParser(object):

    bb_data_query = u"""
        select lokijs.data
        from lokijs
        where lokijs.name = "db.json"
        """

    """
    Returns: 
    A zotero database as an array of Items.
    """

    def load(self, file_path, cache_path):

        if not valid_location(file_path):
            print("{} is not a valid zotero path".format(file_path))
            return []

        self.load_citekeys(file_path, cache_path)

        zotero = zoteroData(file_path, cache_path)
        zot_data = zotero.load()

        items = []
        for zot_id, zot_item in zot_data:

            item = Item()
            item.abstract  = zot_item.abstract
            item.author    = zot_item.format_author()
            item.date      = zot_item.date
            item.doi       = zot_item.doi
            item.file      = zot_item.format_fulltext()
            item.isbn      = zot_item.isbn
            item.publication = zot_item.publication
            item.key       = self.format_key(zot_item.id, zot_item.key)
            item.language  = zot_item.language
            item.issue     = zot_item.issue
            item.notes     = zot_item.format_notes()
            item.pages     = zot_item.pages
            item.publisher = zot_item.publisher
            item.tags      = zot_item.format_tags()
            item.title     = zot_item.title
            item.type      = zot_item.type
            item.url       = zot_item.url
            item.volume    = zot_item.volume
            item.combine()
            items.append(item)
        return items

    def format_key(self, id, key):
        if id in self.citekeys:
            return self.citekeys[id]
        else:
            return key

    def load_citekeys(self, file_path, cache_path):
        """
        Loads better-bibtex citekeys if they exist.
        """
        self.citekeys = {}

        bb_database = os.path.join(file_path, 'betterbibtex-lokijs.sqlite')
        bb_copy = os.path.join(cache_path, 'betterbibtex-lokijs.sqlite')
        shutil.copyfile(bb_database, bb_copy)
        conn = sqlite3.connect(bb_copy)
        cur = conn.cursor()
        cur.execute(self.bb_data_query)
        bb_data = cur.fetchone()[0]
        bb_json = json.loads(bb_data)
        for item in bb_json['collections'][0]['data']:
            self.citekeys[item['itemID']] = item['citekey']

