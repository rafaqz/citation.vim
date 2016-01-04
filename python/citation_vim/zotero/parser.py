# -*- coding: utf-8 -*-

import os
import json
from citation_vim.zotero.data import valid_location, zoteroData
from citation_vim.item import Item

class zoteroParser(object):

    """
    Returns: 
    A zotero database as an array of Items.
    """

    def load(self, source_field, file_path):

        if not valid_location(file_path):
            print("{} is not a valid zotero path".format(file_path))
            return []

        self.load_citekeys(file_path)

        try:
            zotero = zoteroData(file_path)
            zot_data = zotero.load()
        except Exception as e:
            print("Failed to read {}".format(file_path))
            print("Message: {}".format(str(e)))

        items = []
        for zot_id, zot_entry in zot_data:

            item = Item()
            item.abstract  = zot_entry.abstract
            item.author    = zot_entry.format_author()
            item.date      = zot_entry.date
            item.doi       = zot_entry.doi
            item.file      = zot_entry.fulltext
            item.isbn      = zot_entry.isbn
            item.journal   = zot_entry.publication
            item.key       = self.format_key(zot_entry.id, zot_entry.key)
            item.language  = zot_entry.language
            item.issue     = zot_entry.issue
            item.notes     = zot_entry.format_notes()
            item.pages     = zot_entry.pages
            item.publisher = zot_entry.publisher
            item.tags      = zot_entry.format_tags()
            item.title     = zot_entry.title
            item.type      = zot_entry.type
            item.url       = zot_entry.url
            item.volume    = zot_entry.volume
            item.combine()
            if not getattr(item, source_field) == "":
                items.append(item)
        return items


    def format_key(self, id, key):
        if id in self.citekeys:
            return self.citekeys[id]
        else:
            return key

    def load_citekeys(self, file_path):
        """
        Loads better-bibtex citekeys if they exist.
        """
        self.citekeys = {}
        bb_path = os.path.join(file_path, 'better-bibtex/db.json')
        if os.path.exists(bb_path):
            with open(bb_path) as bb:    
                bb_json = json.load(bb)
            for item in bb_json['collections'][0]['data']:
                self.citekeys[item['itemID']] = item['citekey']

