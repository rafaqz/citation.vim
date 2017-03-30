# -*- coding: utf-8 -*-

import os
import json
import shutil
import sqlite3
from citation_vim.zotero.data import ZoteroData
from citation_vim.zotero.betterbibtex import BetterBibtex
from citation_vim.utils import check_path, raiseError
from citation_vim.item import Item

class ZoteroParser(object):

    def __init__(self, context):
        self.context = context
        self.zotero_path = context.zotero_path
        self.cache_path = context.cache_path
        self.et_al_limit = context.et_al_limit
        self.key_format = context.key_format

    def load(self):
        """
        Returns:
        A zotero database as an array of standardised Items.
        """
        if not check_path(os.path.join(self.zotero_path, u"zotero.sqlite")):
            raiseError(u"Citation.vim Error:", self.zotero_path, \
                    u"is not a valid zotero path")
            return []
        zotero = ZoteroData(self.context)
        zot_data = zotero.load()
        bb = BetterBibtex(self.zotero_path, self.cache_path)
        citekeys = bb.load_citekeys()
        return self.build_items(zot_data, citekeys)

    def build_items(self, zot_data, citekeys):
        items = []
        for zot_id, zot_item in zot_data:
            item = Item()
            item.abstract    = zot_item.abstractNote
            item.collections = zot_item.collections
            item.doi         = zot_item.DOI
            item.isbn        = zot_item.ISBN
            item.publication = zot_item.publicationTitle
            item.language    = zot_item.language
            item.issue       = zot_item.issue
            item.pages       = zot_item.pages
            item.publisher   = zot_item.publisher
            item.title       = zot_item.title
            item.type        = zot_item.type
            item.url         = zot_item.url
            item.volume      = zot_item.volume
            item.author      = zot_item.format_author(self.et_al_limit)
            item.date        = zot_item.format_date()
            item.file        = zot_item.format_attachment()
            item.notes       = zot_item.format_notes()
            item.tags        = zot_item.format_tags()
            item.zotero_key  = zot_item.key
            item.key         = self.format_key(item, zot_item, citekeys)
            item.combine()
            items.append(item)

        return items

    def format_key(self, item, zot_item, citekeys):
        """
        Returns:
        A user formatted key if present, or a better bibtex key, or zotero hash.
        """
        if self.context.key_format > "":
            title = item.title.lower()
            title = self.context.key_title_banned_regex.sub("", title)
            title = title.partition(" ")[0]
            date = item.date # Use the allready formatted date
            author = zot_item.format_first_author().replace(" ", "_")
            replacements = {
                u"title": title.lower(),
                u"Title": title.capitalize(), 
                u"author": author.lower(), 
                u"Author": author.capitalize(),
                u"date": date.replace(' ', '-').capitalize() # Date may be 'In-press' 
            }
            key_format = u'%s' % self.context.key_format
            key = key_format.format(**replacements)
            key = self.context.key_clean_regex.sub("", key)
            return key 
        elif zot_item.id in citekeys:
            return citekeys[zot_item.id]
        else:
            return zot_item.key

