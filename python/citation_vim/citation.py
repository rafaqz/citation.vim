# -*- coding: utf-8 -*-

import os.path
import sys

class Citation(object):

    @staticmethod
    def connect():

        """
        Returns source from builder,
        printing any errors from python to the vim console.
        """

        try:
            set_script_path()
            from citation_vim.utils import raiseError
            from citation_vim.builder import Builder
            from citation_vim.context import Context
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
