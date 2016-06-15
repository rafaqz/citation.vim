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
            item.author      = self.format_author(zot_item)
            item.collections = zot_item.collections
            item.date        = zot_item.date
            item.doi         = zot_item.doi
            item.file        = self.format_fulltext(zot_item)
            item.isbn        = zot_item.isbn
            item.publication = zot_item.publication
            item.key         = self.format_key(zot_item, citekeys)
            item.language    = zot_item.language
            item.issue       = zot_item.issue
            item.notes       = self.format_notes(zot_item)
            item.pages       = zot_item.pages
            item.publisher   = zot_item.publisher
            item.tags        = self.format_tags(zot_item)
            item.title       = zot_item.title
            item.type        = zot_item.type
            item.url         = zot_item.url
            item.volume      = zot_item.volume
            item.combine()
            items.append(item)
        return items

    def format_key(self, zot_item, citekeys):
        if zot_item.id in citekeys:
            return citekeys[zot_item.id]
        else:
            return zot_item.key

    def format_author(self, zot_item):

        """
        Returns:
        A pretty representation of the author.
        """

        if zot_item.authors == []:
            return ""
        if len(zot_item.authors) > 5:
            return u"%s et al." % zot_item.authors[0][0]
        if len(zot_item.authors) > 2:
            auth_string = u""
            for author in zot_item.authors[:-1]:
                auth_string += author[0] + ', '
            return auth_string + u"& " + zot_item.authors[-1][0]
        if len(zot_item.authors) == 2:
            return zot_item.authors[0][0] + u" & " + zot_item.authors[1][0]
        return ', '.join(zot_item.authors[0])

    def format_tags(self, zot_item):

        """
        Returns:
        Comma separated tags.
        """

        return u", ".join(zot_item.tags)

    def format_notes(self, zot_item):

        """
        Returns:
        Linebreak separated notes.
        """

        return u"\n\n".join(zot_item.notes)

    def format_fulltext(self, zot_item):

        """
        Returns:
        The first file.
        """

        if zot_item.fulltext == []:
            return ""
        else:
            return zot_item.fulltext[0]
