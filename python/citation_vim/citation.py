# -*- coding: utf-8 -*-

import os.path
import string
import sys
import pickle
from datetime import datetime, timedelta

class Citation(object):

    @staticmethod
    def connect():
        import vim
        script_path = os.path.join(vim.eval('s:script_path'), '../../../python')
        sys.path.insert(0, script_path)

        context = Context()
        context.mode         = vim.eval("g:citation_vim_mode")
        context.bibtex_file  = os.path.expanduser(vim.eval("g:citation_vim_bibtex_file"))
        context.zotero_path  = os.path.expanduser(vim.eval("g:citation_vim_zotero_path"))
        context.cache_path   = os.path.expanduser(vim.eval("g:citation_vim_cache_path"))
        context.desc_format  = vim.eval("g:citation_vim_description_format")
        context.desc_fields  = vim.eval("g:citation_vim_description_fields")
        context.wrap_chars   = vim.eval("g:citation_vim_source_wrap")
        context.source       = vim.eval("a:source")
        context.source_field = vim.eval("a:field")
        context.searchkey    = vim.eval("a:searchkey[0]")
        builder = Builder(context)
        return builder.build_list()

class Context(object):
    'empty context class'

class Builder(object):

    def __init__(self, context, cache = True):
        self.context = context 
        self.zotero_database = os.path.join(self.context.zotero_path, u"zotero.sqlite")
        self.cache_file = os.path.join(self.context.cache_path, u"citation_vim_cache")
        self.cache = cache

    def build_list(self):
        output = []
        for entry in self.get_entries():
            description = self.describe(entry)
            output.append([getattr(entry, self.context.source_field), description])
        return output

    def get_entries(self):
        entries = []
        parser = self.get_parser()
        if self.context.source == 'citation':
            if self.has_cache() and self.cache:
                entries = self.read_cache()
            else:
                entries = parser.load()
                if self.cache:
                    self.write_cache(entries)
        elif self.context.source == 'citation_fulltext':
            entries = parser.load()
        return entries

    def get_parser(self):
        if self.context.mode == "bibtex":
            from citation_vim.bibtex.parser import bibtexParser
            parser = bibtexParser(self.context)
        elif self.context.mode == "zotero":
            from citation_vim.zotero.parser import zoteroParser
            parser = zoteroParser(self.context)
        else:
            print("g:citation_vim_mode must be either 'zotero' or 'bibtex'")
        return parser

    def read_cache(self):
        with open(self.cache_file, 'rb') as in_file:
            return pickle.load(in_file)
        
    def write_cache(self, itemlist):
        with open(self.cache_file, 'wb') as out_file:
            pickle.dump(itemlist, out_file)

    def has_cache(self):
        if not os.path.isfile(self.cache_file):
            return False
        if self.context.mode == 'bibtex':
            file_path = self.bibtex_file
        elif self.context.mode == 'zotero':
            file_path = self.zotero_database
        filetime = datetime.fromtimestamp(os.path.getctime(file_path))
        cachetime = datetime.fromtimestamp(os.path.getctime(self.cache_file))
        return filetime < cachetime

    def describe(self, entry):
        # Get strings for description fields.
        wrap = self.context.wrap_chars
        source_field = self.context.source_field
        desc_fields = self.context.desc_fields
        desc_strings = []
        source_string = u""

        for desc_field in desc_fields:
            try:
                getattr(entry, desc_field)
            except AttributeError:
                return 'Error at "{}" field of g:unite_bibtex_description_fields. Check your vimrc.'.format(desc_field)

            desc_strings.append(getattr(entry, desc_field))

        # Insert the source field if not present in the description,
        # and put brackets around it wherever it is.
        if source_field in desc_fields:
            source_index = desc_fields.index(source_field)
            desc_strings[source_index] = u'%s%s%s' % (wrap[0], desc_strings[source_index], wrap[1])
        else:
            if not source_field in ["combined","file"]:
                source_string = u'%s%s%s' % (wrap[0], getattr(entry, source_field), wrap[1])

        return self.context.desc_format.format(*desc_strings) + source_string
