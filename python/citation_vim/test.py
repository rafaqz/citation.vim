# -*- coding: utf-8 -*-

"""
Tests your citation database in the console

Example *nix style commands:
python test.py /your/bibtext/file bibtex key
python test.py /your/zotero/path zotero key "searchstring" 4
"""

import codecs
import copy
import logging
import sys
import os.path
import re
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, module_path)
from citation_vim.builder import Builder
from citation_vim.context import Context
from citation_vim.utils import compat_str, decode_str
ansi = not sys.platform.startswith("win")

def get_console_context(context):
    context.bibtex_file = sys.argv[1]
    context.zotero_path = sys.argv[1]
    context.mode = sys.argv[2]
    context.source_field = sys.argv[3] 
    if context.mode == u'zotero':
        context.searchkeys = compat_str(sys.argv[4]).split()
        context.zotero_version = int(sys.argv[5])
    return context

def set_default_context(context):
    context.cache_path = ""
    context.collection = ''
    context.source = u'citation'
    context.key_format = u"{author}{date}{Title}"

    context.key_title_banned_regex = re.compile(u"\\b(a|an|the|some|from|on|in|to|of|" "do|with|der|die|das|ein|eine|einer|eines|einem|einen|" "un|une|la|le|l|el|las|los|al|uno|una|unos|unas|de|des|del|d)\\W")
    context.key_clean_regex = re.compile("[^A-Za-z0-9\!\$\&\*\+\-\.\/\:\;\<\>\?\[\]\^\_\`\|]+")
    context.desc_format = u"{}∶ {} ‴{}‴ ₋{}₋ ₍{}₎" 
    context.desc_fields = ["type", "key", "title", "author", "date"]
    context.et_al_limit = 5
    context.wrap_chars = u"||"
    context.zotero_attachment_path = u"~/Zotero/library/"
    context.cache = False
    return context

class col:
    NORMAL = u"\033[m"
    WHITE = u"\033[37m"
    ONE = u"\033[33m"
    TWO = u"\033[32m"
    THREE = u"\033[36m"
    FOUR = u"\033[34m"
    ENDC = u"\033[0m"


def setup_console(sys_enc='utf-8', use_colorama=True):
    """
    Set sys.defaultencoding to `sys_enc` and update stdout/stderr writers to corresponding encoding

    .. note:: For Win32 the OEM console encoding will be used istead of `sys_enc`
    """
    global ansi
    reload(sys)
    try:
        if sys.platform.startswith("win"):
            import ctypes
            enc = "cp%d" % ctypes.windll.kernel32.GetOEMCP()
        else:
            enc = (sys.stdout.encoding if sys.stdout.isatty() else
                        sys.stderr.encoding if sys.stderr.isatty() else
                            sys.getfilesystemencoding() or sys_enc)

        sys.setdefaultencoding(sys_enc)

        if sys.stdout.isatty() and sys.stdout.encoding != enc:
            sys.stdout = codecs.getwriter(enc)(sys.stdout, 'replace')

        if sys.stderr.isatty() and sys.stderr.encoding != enc:
            sys.stderr = codecs.getwriter(enc)(sys.stderr, 'replace')

        if use_colorama and sys.platform.startswith("win"):
            try:
                from colorama import init
                init()
                ansi = True
            except:
                pass

    except:
        pass
        
def print_output(output):
    for field, desc, file, combined in output:
        print(col.ONE + u"\nField: " + col.WHITE + field)
        print(col.TWO + u"\nDescription: ")
        print(col.NORMAL + desc)
        print(col.THREE + u"\nFile: " + col.NORMAL + file)
        print(col.FOUR + u"\nCombined: ")
        print(col.NORMAL + combined)

if sys.version_info[0] == 2:
    setup_console()
context = Context()
context = get_console_context(context)
context = set_default_context(context)
output = Builder(context).build_source()
print_output(output)

