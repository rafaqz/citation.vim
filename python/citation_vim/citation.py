# -*- coding: utf-8 -*-

import os.path
import string
import json
import sys
import pickle
from datetime import datetime, timedelta

class Citation(object):

    @staticmethod
    def get_entries(source_field, file_path, cache_path, file_format, desc_fields, desc_format, wrap_chars):

        file_path = os.path.expanduser(file_path)
        cache_path = os.path.expanduser(cache_path)

        if file_format == "bibtex":
            if Citation.check_cache(file_path, cache_path):
                entries = Citation.load_cache(cache_path)
            else:
                from citation_vim.bibtex.parser import bibtexParser
                parser = bibtexParser()
                entries = parser.load(file_path, cache_path)
                print("hello")
                print(entries)
                Citation.write_cache(entries, cache_path)

        elif file_format == "zotero":
            sqlite_path = os.path.join(file_path, u"zotero.sqlite")
            if Citation.check_cache(sqlite_path, cache_path):
                entries = Citation.load_cache(cache_path)
            else:
                from citation_vim.zotero.parser import zoteroParser
                parser = zoteroParser()
                entries = parser.load(file_path, cache_path)
                Citation.write_cache(entries, cache_path)
        else:
            print("g:citation_vim_file_format variable must be either 'zotero' or 'bibtex'")
            return []


        output = []
        for entry in entries:
            description = Citation.describe(entry, source_field, desc_fields, desc_format, wrap_chars)
            output.append([getattr(entry, source_field), description])
        return output


    @staticmethod
    def connect():
        import vim
        file_format   = vim.eval("g:citation_vim_file_format")
        file_path     = vim.eval("g:citation_vim_file_path")
        cache_path    = vim.eval("g:citation_vim_cache_path")
        desc_format   = vim.eval("g:citation_vim_description_format")
        desc_fields   = vim.eval("g:citation_vim_description_fields")
        wrap_chars    = vim.eval("g:citation_vim_source_wrap")
        source_field  = vim.eval("a:field")
        script_folder = os.path.join(vim.eval('s:script_folder_path'), '../../../python')
        sys.path.insert(0, script_folder)

        return Citation.get_entries(source_field, file_path, cache_path, file_format, desc_fields, desc_format, wrap_chars)

    @staticmethod
    def load_cache(cache_path):
        with open(Citation.cache_file(cache_path), 'rb') as in_file:
            return pickle.load(in_file)
        
    @staticmethod
    def write_cache(itemlist, cache_path):
        with open(Citation.cache_file(cache_path), 'wb') as out_file:
            pickle.dump(itemlist, out_file)

    @staticmethod
    def cache_file(cache_path):
        return os.path.join(cache_path, u"citation_vim_cache")

    @staticmethod
    def check_cache(file_path, cache_path):
        cache_file = Citation.cache_file(cache_path)
        if not os.path.isfile(cache_file):
            return False
        cachetime = datetime.fromtimestamp(os.path.getctime(cache_file))
        filetime = datetime.fromtimestamp(os.path.getctime(file_path))
        return filetime < cachetime


    @staticmethod
    def describe(entry, source_field, desc_fields, desc_format, wrap_chars):
        # Get strings for description fields.
        desc_strings = []
        for desc_field in desc_fields:
            try:
                getattr(entry, desc_field)
            except AttributeError:
                return 'Error at "{}" field of g:unite_bibtex_description_fields. Check your vimrc.'.format(desc_field)

            desc_strings.append(getattr(entry, desc_field))

        # Insert the source field if not present in the description,
        # and put brackets around it wherever it is.
        source_string = u""
        if source_field in desc_fields:
            source_index = desc_fields.index(source_field)
            desc_strings[source_index] = u'%s%s%s' % (wrap_chars[0], desc_strings[source_index], wrap_chars[1])
        else:
            if not source_field in ["combined","file"]:
                source_string = u'%s%s%s' % (wrap_chars[0], getattr(entry, source_field), wrap_chars[1])

        return desc_format.format(*desc_strings) + source_string
