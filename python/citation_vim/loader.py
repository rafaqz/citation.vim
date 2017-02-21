# -*- coding: utf-8 -*-

import os.path
import vim
from citation_vim.utils import raiseError

def get_vim_context(context):

    context.mode = vim.eval("g:citation_vim_mode")
    if context.mode == "bibtex":
        context.bibtex_file = get_bibtex_file()
    elif context.mode == "zotero":
        context.zotero_path = get_zotero_path()
    else:
        raiseError(u"'g:citation_vim_mode' must be set to 'zotero' or 'bibtex'")

    context.cache_path = get_cache_path()
    context.collection   = vim.eval("g:citation_vim_collection")
    context.key_format   = vim.eval("g:citation_vim_key_format")
    context.desc_format  = vim.eval("g:citation_vim_description_format")
    context.desc_fields  = vim.eval("g:citation_vim_description_fields")
    context.wrap_chars   = vim.eval("g:citation_vim_source_wrap")
    context.et_al_limit  = int(vim.eval("g:citation_vim_et_al_limit"))
    context.zotero_version = int(vim.eval("g:citation_vim_zotero_version"))
    context.source       = vim.eval("a:source")
    context.source_field = vim.eval("a:field")

    context.searchkeys = get_searchkeys()
    context.cache = can_cache(context.searchkeys)

    return context

def get_zotero_path():
    try:
        file = vim.eval("g:citation_vim_zotero_path")
        return os.path.expanduser(file)
    except:
        raiseError(u"global variable 'g:citation_vim_zotero_path' is not set")

def get_bibtex_file():
    try:
        file = vim.eval("g:citation_vim_bibtex_file")
        return os.path.expanduser(file)
    except:
        raiseError(u"'g:citation_vim_bibtex_file' is not set")

def get_cache_path():
    try:
        return os.path.expanduser(vim.eval("g:citation_vim_cache_path"))
    except:
        raiseError(u"'g:citation_vim_cache_path' is not set")

def get_searchkeys():
    searchkeys = vim.eval("l:searchkeys")
    if len(searchkeys) > 0:
        return searchkeys.split()
    return []

def can_cache(searchkeys):
    if searchkeys > []:
        return True
    return False
