# -*- coding: utf-8 -*-

import os
import json
import shutil
import sqlite3
from citation_vim.zotero.data import zoteroData
from citation_vim.zotero.betterbibtex import betterBibtex
from citation_vim.utils import check_path, raiseError
from citation_vim.item import Item

class zoteroParser(object):

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

        zotero = zoteroData(self.context)
        zot_data = zotero.load()
        bb = betterBibtex(self.zotero_path, self.cache_path)
        citekeys = bb.load_citekeys()

        items = []
        for zot_id, zot_item in zot_data:
            item = Item()
            item.abstract    = zot_item.abstract
            item.collections = zot_item.collections
            item.doi         = zot_item.doi
            item.isbn        = zot_item.isbn
            item.publication = zot_item.publication
            item.language    = zot_item.language
            item.issue       = zot_item.issue
            item.pages       = zot_item.pages
            item.publisher   = zot_item.publisher
            item.title       = zot_item.title
            item.type        = zot_item.type
            item.url         = zot_item.url
            item.volume      = zot_item.volume
            item.author      = self.format_author(zot_item)
            item.date        = self.format_date(zot_item)
            item.file        = self.format_fulltext(zot_item)
            item.notes       = self.format_notes(zot_item)
            item.tags        = self.format_tags(zot_item)
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
            title = zot_item.title.partition(' ')[0]
            author = self.format_first_author(zot_item)
            replacements = {
                u"title": title.lower(),
                u"Title": title.capitalize(), 
                u"author": author.lower(), 
                u"Author": author.capitalize(),
                u"date": item.date.replace(' ', '-').capitalize() # Date may be 'In-press' 
            }
            key_format = u'%s' % self.context.key_format
            return key_format.format(**replacements)
        elif zot_item.id in citekeys:
            return citekeys[zot_item.id]
        else:
            return zot_item.key

    def format_first_author(self, zot_item):
        """
        Returns: The first authors surname, if one exists.
        """
        if zot_item.authors == []:
            return ""
        return zot_item.authors[0][0]
        
    def format_author(self, zot_item):
        """
        Returns: A pretty representation of the author.
        """
        if zot_item.authors == []:
            return ""
        if len(zot_item.authors) > self.et_al_limit:
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
        Returns: Comma separated tags.
        """
        return u", ".join(zot_item.tags)

    def format_notes(self, zot_item):
        """
        Returns: Linebreak separated notes.
        """
        return u"\n\n".join(zot_item.notes)

    def format_fulltext(self, zot_item):
        """
        Returns: The first file.
        """
        if zot_item.fulltext == []:
            return ""
        else:
            return zot_item.fulltext[0]

    def format_date(self, zot_item):
        """
        Returns: The year or special string.
        """
        # Some dates are treated as special and are not parsed into a year
        # representation
        special_dates = u"in press", u"submitted", u"in preparation", \
            u"unpublished"
        for specialdate in special_dates:
            if specialdate in zot_item.date.lower():
                return specialdate

        # Dates can have months, days, and years, or just a
        # year, and can be split by '-' and '/' characters.
        # Detect whether the date should be split
        date = ""
        if u'/' in zot_item.date:
            split = u'/'
        elif u'-' in zot_item.date:
            split = u'-'
        else:
            split = None
        # If not, just use the last four characters
        if split == None:
            date = zot_item.date[-4:]
        # Else take the first slice that is four characters
        else:
            l = zot_item.date.split(split)
            for i in l:
                if len(i) == 4:
                    date = i
                    break
        return date
