# -*- coding: utf-8 -*-

import os.path
import vim
import re
import sys
from citation_vim.utils import raiseError, decode_str
from citation_vim.context import Context

class Loader(object):

    """
    Loads context from Vim
    """

    def context():
        return self.context

    def __init__(self):
        context = Context()
        context = self.get_mode(context)
        context = self.get_shared_context(context)
        self.context = context

    def get_mode(self, context):
        context.mode = vim.eval("g:citation_vim_mode")
        if context.mode == "bibtex":
            context = self.get_bibtex_context(context)
        elif context.mode == "zotero":
            context = self.get_zotero_context(context)
        else:
            raiseError(u"'g:citation_vim_mode' must be set to 'zotero' or 'bibtex'")
        return context

    def get_bibtex_context(self, context):
        context.bibtex_file = self.get_bibtex_file()
        context.cache = True
        return context

    def get_zotero_context(self, context):
        context.zotero_version = int(vim.eval(u"g:citation_vim_zotero_version"))
        context.zotero_path = self.get_zotero_path()
        context.zotero_attachment_path = self.get_zotero_attachment_path()
        context.searchkeys = self.get_searchkeys()
        context.cache = self.can_cache(context.searchkeys)
        return context

    def get_shared_context(self, context):
        context.key_clean_regex        = re.compile(decode_str(vim.eval("g:citation_vim_key_clean_regex")))
        context.key_title_banned_regex = re.compile(decode_str(vim.eval("g:citation_vim_key_title_banned_regex")))
        context.collection   = decode_str(vim.eval("g:citation_vim_collection"))
        context.key_format   = decode_str(vim.eval("g:citation_vim_key_format"))
        context.wrap_chars   = decode_str(vim.eval("g:citation_vim_source_wrap"))
        context.desc_format  = decode_str(vim.eval("g:citation_vim_description_format"))
        context.desc_fields  = vim.eval("g:citation_vim_description_fields")
        context.source       = vim.eval("a:source")
        context.source_field = vim.eval("a:field")
        context.et_al_limit  = int(vim.eval("g:citation_vim_et_al_limit"))
        context.cache_path   = self.get_cache_path()
        return context

    def get_zotero_path(self):
        try:
            file = vim.eval("g:citation_vim_zotero_path")
            return os.path.expanduser(file)
        except:
            raiseError("global variable 'g:citation_vim_zotero_path' is not set")

    def get_bibtex_file(self):
        try:
            file = vim.eval("g:citation_vim_bibtex_file")
            return os.path.expanduser(file)
        except:
            raiseError("'g:citation_vim_bibtex_file' is not set")

    def get_zotero_attachment_path(self):
        file = vim.eval("g:citation_vim_zotero_attachment_path")
        return os.path.expanduser(file)

    def get_cache_path(self):
        try:
            return os.path.expanduser(vim.eval("g:citation_vim_cache_path"))
        except:
            raiseError("'g:citation_vim_cache_path' is not set")

    def get_searchkeys(self):
        searchkeys = vim.eval("l:searchkeys")
        if len(searchkeys) > 0:
            return searchkeys.split()
        return []

    def can_cache(self, searchkeys):
        if searchkeys == []:
            return True
        return False
