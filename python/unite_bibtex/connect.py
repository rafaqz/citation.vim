# -*- coding: utf-8 -*-

import os.path
import string
import json
import sys
sys.path.insert( 0, "/home/raf/.vim/plugged/unite-bibtex/python")
from unite_bibtex.zotero.parser import zoteroParser
from unite_bibtex.bibtex.parser import bibtexParser

class uniteBibtex(object):

    @staticmethod
    def get_entries(field, file_path, file_format, desc_fields, desc_format):
        if file_format == "bibtex":
            parser = bibtexParser()
        elif file_format == "zotero":
            parser = zoteroParser()
        else:
            print("g:unite_bibtex_file_format variable must be either 'zotero' or 'bibtex'")
            return []
        entries = parser.load(field, file_path)
        output = []
        for entry in entries:
            desc = entry.describe(field, desc_fields, desc_format)
            output.append([eval("entry." + field), desc])
        return output


    @staticmethod
    def connect():
        import vim
        file_format = vim.eval("g:unite_bibtex_file_format")
        file_path   = vim.eval("g:unite_bibtex_file_path")
        desc_format = vim.eval("g:unite_bibtex_description_format")
        desc_fields = vim.eval("g:unite_bibtex_description_fields")
        field       = vim.eval("a:field")
        script_folder = vim.eval('s:script_folder_path')
        script_folder = os.path.join(script_folder, '../../../python') 
        print(script_folder)
        sys.path.insert(0, script_folder)

        return uniteBibtex.get_entries(field, file_path, file_format, desc_fields, desc_format)

