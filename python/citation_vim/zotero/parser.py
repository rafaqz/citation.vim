# -*- coding: utf-8 -*-

import os
import json
import shutil
import sqlite3
from citation_vim.zotero.data import valid_location, zoteroData
from citation_vim.zotero.betterbibtex import betterBibtex
from citation_vim.item import Item

class zoteroParser(object):

    """
    Returns: 
    A zotero database as an array of Items.
    """

    def __init__(self, context):
        self.context = context
        self.zotero_path = context.zotero_path
        self.cache_path = context.cache_path

    def load(self):

        if not valid_location(self.zotero_path):
            print("{} is not a valid zotero path".format(zotero_path))
            return []

        zotero = zoteroData(self.context)
        zot_data = zotero.load()
        bb = betterBibtex(self.zotero_path, self.cache_path)
        citekeys = bb.load_citekeys()

        items = []
        for zot_id, zot_item in zot_data:
            item = Item()
            item.abstract    = zot_item.abstract
            item.author      = zot_item.format_author()
            item.date        = zot_item.date
            item.doi         = zot_item.doi
            item.file        = zot_item.format_fulltext()
            item.isbn        = zot_item.isbn
            item.publication = zot_item.publication
            item.key         = self.format_key(zot_item, citekeys)
            item.language    = zot_item.language
            item.issue       = zot_item.issue
            item.notes       = zot_item.format_notes()
            item.pages       = zot_item.pages
            item.publisher   = zot_item.publisher
            item.tags        = zot_item.format_tags()
            item.title       = zot_item.title
            item.type        = zot_item.type
            item.url         = zot_item.url
            item.volume      = zot_item.volume
            item.combine()
            items.append(item)
        return items

    def format_key(self, item, citekeys):
        if item.id in citekeys:
            return citekeys[item.id]
        else:
            return item.key
