# -*- coding: utf-8 -*-

import os.path
import sys
import vim

class Citation(object):

    @staticmethod
    def connect():

        """
        Returns source from builder,
        printing any errors from python to the vim console.

        wrapping everything in "try: except:" is bad practise generally, 
        but in this case ensures all erros can actually be reported 
        """

        try:
            set_script_path()
            from citation_vim.builder import Builder
            from citation_vim.loader import Loader
            return Builder(Loader().context).build_source()
        except:
            print_exception()

def set_script_path():
    script_path = os.path.join(vim.eval('s:script_path'), '../../../python')
    sys.path.insert(0, script_path)

def print_exception():
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    print("Citation.vim error:\n" + "".join(line for line in lines))
