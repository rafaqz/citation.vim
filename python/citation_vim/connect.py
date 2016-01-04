# -*- coding: utf-8 -*-

import os.path
import string
import json
import sys

class Citation(object):

    @staticmethod
    def get_entries(source_field, file_path, file_format, desc_fields, desc_format):
        if file_format == "bibtex":
            from citation_vim.bibtex.parser import bibtexParser
            parser = bibtexParser()
        elif file_format == "zotero":
            from citation_vim.zotero.parser import zoteroParser
            parser = zoteroParser()
        else:
            print("g:citation_vim_file_format variable must be either 'zotero' or 'bibtex'")
            return []
        entries = parser.load(source_field, file_path)
        output = []
        for entry in entries:
            desc = entry.describe(source_field, desc_fields, desc_format)
            output.append([getattr(entry, source_field), desc])
        return output


    @staticmethod
    def connect():
        import vim
        file_format   = vim.eval("g:citation_vim_file_format")
        file_path     = vim.eval("g:citation_vim_file_path")
        desc_format   = vim.eval("g:citation_vim_description_format")
        desc_fields   = vim.eval("g:citation_vim_description_fields")
        source_field  = vim.eval("a:field")
        script_folder = os.path.join(vim.eval('s:script_folder_path'), '../../../python')
        sys.path.insert(0, script_folder)

        return Citation.get_entries(source_field, file_path, file_format, desc_fields, desc_format)

