# -*- coding: utf-8 -*-

import os.path
import string
import sys
import pickle

class Citation(object):

    @staticmethod
    def connect():
        import vim
        script_path = os.path.join(vim.eval('s:script_path'), '../../../python')
        sys.path.insert(0, script_path)
        from citation_vim.utils import raiseError

        context = Context()
        context.mode = vim.eval("g:citation_vim_mode")
        if context.mode == "bibtex":
            try:
                file = vim.eval("g:citation_vim_bibtex_file")
                context.bibtex_file  = os.path.expanduser(file)
            except:
                raiseError(u"Citation.vim Error: global variable 'g:citation_vim_bibtex_file' is not set")
        elif context.mode == "zotero":
            try:
                file = vim.eval("g:citation_vim_zotero_path")
                context.zotero_path = os.path.expanduser(file)
            except:
                raise(u"Citation.vim Error: global variable 'g:citation_vim_zotero_path' is not set")
        else:
            raiseError(u"Citation.vim Error: global variable 'g:citation_vim_mode' must be set to 'zotero' or 'bibtex'")

        try:
            context.cache_path = os.path.expanduser(vim.eval("g:citation_vim_cache_path"))
        except:
            raiseError(u"Citation.vim Error: global variable 'g:citation_vim_cache_path' is not set")

        context.collection   = vim.eval("g:citation_vim_collection")
        context.key_format   = vim.eval("g:citation_vim_key_format")
        context.desc_format  = vim.eval("g:citation_vim_description_format")
        context.desc_fields  = vim.eval("g:citation_vim_description_fields")
        context.wrap_chars   = vim.eval("g:citation_vim_source_wrap")
        context.et_al_limit  = vim.eval("g:citation_vim_et_al_limit")
        context.zotero_version = int(vim.eval("g:citation_vim_zotero_version"))
        context.source       = vim.eval("a:source")
        context.source_field = vim.eval("a:field")
        searchkeys = vim.eval("l:searchkeys")
        if len(searchkeys) > 0:
            context.searchkeys = searchkeys.split()
        else:
            context.searchkeys = []

        builder = Builder(context)
        return builder.build_list()
        return []

class Context(object):
    'empty context class'

class Builder(object):

    def __init__(self, context, cache = True):
        self.context = context
        self.cache_file = os.path.join(self.context.cache_path, u"citation_vim_cache")
        self.cache = cache

    def build_list(self):
        if self.context.source == 'citation_collection':
            return self.get_collections()
        else:
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
        output = [["<all>",""]]
        collections = {}
        for item in self.get_items():
            for col in item.collections:
                if not col in collections:
                    output.append([col, col])
                    collections[col] = col
        return output

    def get_items(self):
        parser = self.get_parser()

        if len(self.context.searchkeys) > 0:
            return parser.load()

        if self.has_cache() and self.cache:
            try:
                items = self.read_cache()
            except:
                items = []
            else:
                return items

        items = parser.load()
        if self.cache:
            self.write_cache(items)
        return items

    def get_parser(self):
        if self.context.mode == "bibtex":
            from citation_vim.bibtex.parser import bibtexParser
            parser = bibtexParser(self.context)
        elif self.context.mode == "zotero":
            from citation_vim.zotero.parser import zoteroParser
            parser = zoteroParser(self.context)
        else:
            raiseError(u"Citation.vim Error: g:citation_vim_mode must be either 'zotero' or 'bibtex'")
        return parser

    def read_cache(self):
        try:
            with open(self.cache_file, 'rb') as in_file:
                return pickle.load(in_file)
        except Exception as e:
            raiseError(u"citation_vim.citation.write_cache(): %s" % e)

    def write_cache(self, itemlist):
        try:
            with open(self.cache_file, 'wb') as out_file:
                pickle.dump(itemlist, out_file)
        except Exception as e:
            raiseError(u"citation_vim.citation.write_cache(): %s" % e)



    def has_cache(self):
        from citation_vim.utils import is_current
        if self.context.mode == 'bibtex':
            file_path = self.context.bibtex_file
        elif self.context.mode == 'zotero':
            zotero_database = os.path.join(self.context.zotero_path, u"zotero.sqlite")
            file_path = zotero_database
        return is_current(file_path, self.cache_file)


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
