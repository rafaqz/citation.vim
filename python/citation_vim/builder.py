# -*- coding: utf-8 -*-

import os.path
import string
import pickle
from citation_vim.utils import raiseError

class Builder(object):
    
    def __init__(self, context):
        self.context = context
        self.cache_file = os.path.join(self.context.cache_path, u"citation_vim_cache")
        self.cache = context.cache

    def build_source(self):
        """
        Returns source array.
        """
        if self.context.source == 'citation_collection':
            return self.get_collections()

        output = []
        for item in self.get_items():
            if self.context.collection == "" or self.context.collection in item.collections:
                description = self.describe(item)
                output.append([
                    getattr(item, self.context.source_field),
                    description,
                    item.file,
                    item.combined,
                ])
        return output

    def get_collections(self):
        """
        Returns an array of collections.
        """
        output = ["<all>"]
        collections = {}
        for item in self.get_items():
            for col in item.collections:
                if not col in collections:
                    output.append(col)
                    collections[col] = col
        return output

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
            from citation_vim.bibtex.parser import bibtexParser
            parser = bibtexParser(self.context)
        elif self.context.mode == "zotero":
            from citation_vim.zotero.parser import zoteroParser
            parser = zoteroParser(self.context)
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
        return is_current(file_path, self.cache_file)

    def describe(self, item):
        """
        Returns visible text descriptions for unite, from user selected fields.
        """
        description_values = self.get_description_values(item)
        return self.describe_with_source_field(description_values, item)

    def get_description_values(self, item):
        description_fields = self.context.desc_fields
        description_values = []
        for description_field in description_fields:
            if hasattr(item, description_field):
                description_values.append(getattr(item, description_field))
            else:
                description_values.append("")
        return description_values

    def describe_with_source_field(self, description_values, item):
        """
        Returns description with added/replaced wrapped source field
        """
        description_fields = self.context.desc_fields
        description_format = self.context.desc_format
        source_field = self.context.source_field
        wrapper = self.context.wrap_chars
        if hasattr(item, source_field):
            source_value = getattr(item, source_field)
        else: 
            source_value = ""
        wrapped_source = self.wrap_string(source_value, wrapper)
        if source_field in description_fields:
            source_index = description_fields.index(source_field)
            description_values[source_index] = wrapped_source
        elif not source_field in ["combined"]:
            description_format += wrapped_source
        return description_format.format(*description_values)

    def wrap_string(self, string, wrapper):
        return u'%s%s%s' % (wrapper[0], string, wrapper[1])
