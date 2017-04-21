# -*- coding: utf-8 -*-

import os.path
import string
import pickle
from citation_vim.utils import raiseError
from citation_vim.item import Item

class Builder(object):
    
    def __init__(self, context):
        self.context = context
        self.cache_file = os.path.join(self.context.cache_path, u"citation_vim_cache")
        self.cache = context.cache

    def build_source(self):
        """
        Returns source array depending, on source and field.
        """
        if self.context.source == 'citation_collection':
            return self.get_collections()
        elif self.context.source_field == 'duplicate_keys':
            return self.get_duplicate_keys()
        else:
            return self.get_sub_source()

    def get_sub_source(self):
        output = []
        for item in self.get_items():
            if self.context.collection == "" or self.context.collection in item.collections:
                output.append(self.item_to_array(item))
        return output

    def get_collections(self):
        """
        Returns an array of collections.
        """
        output = [""]
        collections = {}
        for item in self.get_items():
            for col in item.collections:
                if not col in collections:
                    output.append(col)
                    collections[col] = col
        return output

    def get_duplicate_keys(self):
        """
        Returns an array of collections.
        """
        self.context.collection = ""
        self.context.cache = False
        self.context.source_field = 'key'
        return self.filter_duplicate_keys()

    def filter_duplicate_keys(self):
        items = self.get_items()
        items.sort(key = lambda item: item.key)
        last_item = Item()
        last_item.key = ""
        output = []
        for item in items:
            if last_item.key == item.key:
                output.append(self.item_to_array(item))
            last_item = item
        return output

    def item_to_array(self, item):
        return [
            getattr(item, self.context.source_field),
            item.describe(self.context),
            item.file,
            item.combined,
        ]

    def get_items(self):
        """
        Returns items from cache or parser 
        """
        if self.cache and self.is_cached(): 
            return self.read_cache()
        parser = self.get_parser()
        items = parser.load()
        if self.cache:
            self.write_cache(items)
        return items

    def get_parser(self):
        """
        Returns a bibtex or zotero parser.
        """
        if self.context.mode == "bibtex":
            from citation_vim.bibtex.parser import BibtexParser
            parser = BibtexParser(self.context)
        elif self.context.mode == "zotero":
            from citation_vim.zotero.parser import ZoteroParser
            parser = ZoteroParser(self.context)
        else:
            raiseError(u"g:citation_vim_mode must be either 'zotero' or 'bibtex'")
        return parser

    def read_cache(self):
        """
        Returns items from the cache file.
        """
        try:
            with open(self.cache_file, 'rb') as in_file:
                return pickle.load(in_file)
        except:
            raiseError(u"Cache could not be read")

    def write_cache(self, items):
        """
        Writes the cache file.
        """
        try:
            with open(self.cache_file, 'wb') as out_file:
                pickle.dump(items, out_file)
        except: 
            raiseError(u"Cache could not be written")

    def is_cached(self):
        """
        Returns boolean based on cache and target file dates
        """
        from citation_vim.utils import is_current
        if self.context.mode == 'bibtex':
            file_path = self.context.bibtex_file
        elif self.context.mode == 'zotero':
            zotero_database = os.path.join(self.context.zotero_path, u"zotero.sqlite") 
            file_path = zotero_database
        else: 
            raiseError(u"g:citation_vim_mode must be either 'zotero' or 'bibtex'")
        return is_current(file_path, self.cache_file)
