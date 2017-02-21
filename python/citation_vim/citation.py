# -*- coding: utf-8 -*-

import os.path
import sys

class Citation(object):

    @staticmethod
    def connect():

        """
        Loads variables from vimscript and returns the source array.
        Prints errors from python to appear in the vim console.
        """

        try:
            import vim
            script_path = os.path.join(vim.eval('s:script_path'), '../../../python')
            sys.path.insert(0, script_path)
            from citation_vim.utils import raiseError
            from citation_vim.builder import Builder
            from citation_vim.builder import Context

            context = Context()
            context.mode = vim.eval("g:citation_vim_mode")
            if context.mode == "bibtex":
                try:
                    file = vim.eval("g:citation_vim_bibtex_file")
                    context.bibtex_file  = os.path.expanduser(file)
                except:
                    raiseError(u"global variable 'g:citation_vim_bibtex_file' is not set")
            elif context.mode == "zotero":
                try:
                    file = vim.eval("g:citation_vim_zotero_path")
                    context.zotero_path = os.path.expanduser(file)
                except:
                    raiseError(u"global variable 'g:citation_vim_zotero_path' is not set")
            else:
                raiseError(u"global variable 'g:citation_vim_mode' must be set to 'zotero' or 'bibtex'")

            try:
                context.cache_path = os.path.expanduser(vim.eval("g:citation_vim_cache_path"))
            except:
                raiseError(u"global variable 'g:citation_vim_cache_path' is not set")

            context.collection   = vim.eval("g:citation_vim_collection")
            context.key_format   = vim.eval("g:citation_vim_key_format")
            context.desc_format  = vim.eval("g:citation_vim_description_format")
            context.desc_fields  = vim.eval("g:citation_vim_description_fields")
            context.wrap_chars   = vim.eval("g:citation_vim_source_wrap")
            context.et_al_limit  = vim.eval("g:citation_vim_et_al_limit")
            context.zotero_version = int(vim.eval("g:citation_vim_zotero_version"))
            context.source       = vim.eval("a:source")
            context.source_field = vim.eval("a:field")

            context.cache = True
            searchkeys_string = vim.eval("l:searchkeys")
            if len(searchkeys_string) > 0:
                context.cache = False
                context.searchkeys = searchkeys_string.split()
            else:
                context.searchkeys = []

            builder = Builder(context)
            return builder.build_source()

        except:
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print("Citation.vim error:\n" + "".join(line for line in lines))

