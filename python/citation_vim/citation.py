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
        script_folder = os.path.join(vim.eval('s:script_folder_path'), '../../../python')
        sys.path.insert(0, script_folder)

        context = Citation.Context()
        context.file_format   = vim.eval("g:citation_vim_file_format")
        context.bibtex_file   = vim.eval("g:citation_bibtex_file")
        context.zotero_folder = vim.eval("g:citation_zotero_folder")
        context.cache_path    = vim.eval("g:citation_vim_cache_path")
        context.desc_format   = vim.eval("g:citation_vim_description_format")
        context.desc_fields   = vim.eval("g:citation_vim_description_fields")
        context.wrap_chars    = vim.eval("g:citation_vim_source_wrap")
        context.source        = vim.eval("a:source")
        context.source_field  = vim.eval("a:field")
        builder = Citation.Builder(context)
        return builder.build_list()

    class Context(object):
        'empty context class'

    class Builder(object):

        def __init__(self, context):
            self.context = context 
            self.bibtex_file = os.path.expanduser(context.bibtex_file)
            self.zotero_folder = os.path.expanduser(context.zotero_folder)
            self.zotero_database = os.path.join(self.zotero_folder, u"zotero.sqlite")
            self.cache_path = os.path.expanduser(context.cache_path)
            self.cache_file = os.path.join(self.cache_path, u"citation_vim_cache")

        def build_list(self):
            output = []
            for entry in self.get_entries():
                description = self.describe(entry)
                output.append([getattr(entry, self.context.source_field), description])
            return output

        def get_entries(self):
            entries = []
            if self.has_cache():
                entries = self.load_cache()
            else:
                parser = self.get_parser()
                entries = parser.load()
                self.write_cache(entries)
            return entries

        def get_parser(self):
            if self.context.file_format == "bibtex":
                from citation_vim.bibtex.parser import bibtexParser
                parser = bibtexParser(self.bibtex_file)
            elif self.context.file_format == "zotero":
                from citation_vim.zotero.parser import zoteroParser
                parser = zoteroParser(self.zotero_folder, self.cache_path)
            else:
                print("g:citation_vim_file_format variable must be either 'zotero' or 'bibtex'")
            return parser

        def load_cache(self):
            with open(self.cache_file, 'rb') as in_file:
                return pickle.load(in_file)
            
        def write_cache(self, itemlist):
            with open(self.cache_file, 'wb') as out_file:
                pickle.dump(itemlist, out_file)

        def has_cache(self):
            if not os.path.isfile(self.cache_file):
                return False
            if self.context.file_format == 'bibtex':
                file_path = self.bibtex_file
            elif self.context.file_format == 'zotero':
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
