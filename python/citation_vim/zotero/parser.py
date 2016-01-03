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

    def load(self, field, file_path):

        if not valid_location(file_path):
            print("{} is not a valid zotero path".format(file_path))
            return []

        self.load_citekeys(file_path)

        try:
            zotero = zoteroData(file_path)
            data = zotero.load()
        except Exception as e:
            print("Failed to read {}".format(file_path))
            print("Message: {}".format(str(e)))

        items = []
        for entry_id, entry in data:

            item = Item()
            item.abstract  = entry.abstract,
            item.author    = entry.format_author()
            item.date      = entry.date
            item.doi       = entry.doi
            item.file      = entry.fulltext
            item.isbn      = entry.isbn
            item.journal   = entry.publication
            item.key       = self.format_key(entry.id, entry.key)
            item.language  = entry.language
            item.issue     = entry.issue
            item.notes     = entry.format_notes()
            item.pages     = entry.pages
            item.publisher = entry.publisher
            item.tags      = entry.format_tags()
            item.title     = entry.title
            item.type      = entry.type
            item.url       = entry.url
            item.volume    = entry.volume
            item.combine()
            
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

