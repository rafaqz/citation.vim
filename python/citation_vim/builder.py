# -*- coding: utf-8 -*-

import os.path
import string
import pickle

class Context(object):
    'empty context class'

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
                output.append([getattr(item, self.context.source_field),
                               description,
                               item.file,
                               item.combined,
                ])
        return output

    def get_collections(self):
        """
        Returns an array of collections.
        """
        output = [["<all>",""]]
        collections = {}
        for item in self.get_items():
            for col in item.collections:
                if not col in collections:
                    output.append([col, col])
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
        wrap = self.context.wrap_chars
        source_field = self.context.source_field
        desc_fields = self.context.desc_fields
        desc_strings = []
        source_string = u""

        for desc_field in desc_fields:
            try:
                getattr(item, desc_field)
            except AttributeError:
                raiseError('"{}" in g:citation_vim_description_fields.'.format(desc_field))
            desc_strings.append(getattr(item, desc_field))

        # Insert the source field if not present in the description.
        # Put brackets around it wherever it is.
        if source_field in desc_fields:
            source_index = desc_fields.index(source_field)
            desc_strings[source_index] = u'%s%s%s' % (wrap[0], desc_strings[source_index], wrap[1])
        else:
            if not source_field in ["combined","file"]:
                source_string = u'%s%s%s' % (wrap[0], getattr(item, source_field), wrap[1])

        return self.context.desc_format.format(*desc_strings) + source_string
