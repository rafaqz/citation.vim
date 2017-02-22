# -*- coding: utf-8 -*-

import os.path
import vim
from citation_vim.utils import raiseError
from citation_vim.context import Context

class Loader(object):

    def context():
        return self.context

    def __init__(self):
        context = self.set_mode()

        context.cache_path = self.get_cache_path()
        context.collection = vim.eval("g:citation_vim_collection")
        context.key_format = vim.eval("g:citation_vim_key_format")
        context.desc_format = vim.eval("g:citation_vim_description_format")
        context.desc_fields = vim.eval("g:citation_vim_description_fields")
        context.wrap_chars = vim.eval("g:citation_vim_source_wrap")
        context.et_al_limit = int(vim.eval("g:citation_vim_et_al_limit"))
        context.source = vim.eval("a:source")
        context.source_field = vim.eval("a:field")
        self.context = context

    def set_mode(self):
        context = Context()
        context.mode = vim.eval("g:citation_vim_mode")
        if context.mode == "bibtex":
            context.bibtex_file = self.get_bibtex_file()
            context.cache = True
        elif context.mode == "zotero":
            context.zotero_version = int(vim.eval("g:citation_vim_zotero_version"))
            context.zotero_path = self.get_zotero_path()
            context.zotero_attachment_path = self.get_zotero_attachment_path()
            context.searchkeys = self.get_searchkeys()
            context.cache = self.can_cache(context.searchkeys)
        else:
            raiseError(u"'g:citation_vim_mode' must be set to 'zotero' or 'bibtex'")
        return context

    def get_zotero_path(self):
        try:
            file = vim.eval("g:citation_vim_zotero_path")
            return os.path.expanduser(file)
        except:
            raiseError(u"global variable 'g:citation_vim_zotero_path' is not set")

    def get_bibtex_file(self):
        try:
            file = vim.eval("g:citation_vim_bibtex_file")
            return os.path.expanduser(file)
        except:
            raiseError(u"'g:citation_vim_bibtex_file' is not set")

    def get_zotero_attachment_path(self):
        file = vim.eval("g:citation_vim_zotero_attachment_path")
        return os.path.expanduser(file)

    def get_cache_path(self):
        try:
            return os.path.expanduser(vim.eval("g:citation_vim_cache_path"))
        except:
            raiseError(u"'g:citation_vim_cache_path' is not set")

    def get_searchkeys(self):
        searchkeys = vim.eval("l:searchkeys")
        if len(searchkeys) > 0:
            return searchkeys.split()
        return []

    def can_cache(self, searchkeys):
        if searchkeys == []:
            return True
        return False
