# -*- coding: utf-8 -*-

import os.path
import sys

class Citation(object):

    @staticmethod
    def connect():

        """
        Loads variables from vimscript and passes them to the builder.
        Prints errors from python to appear in the vim console.
        """

        try:
            script_path = os.path.join(vim.eval('s:script_path'), '../../../python')
            sys.path.insert(0, script_path)
            from citation_vim.utils import raiseError
            from citation_vim.builder import Builder
            from citation_vim.context import Context
            from citation_vim.loader import get_vim_context

            context = get_vim_context(Context())
            builder = Builder(context)
            return builder.build_source()

        except:
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print("Citation.vim error:\n" + "".join(line for line in lines))
