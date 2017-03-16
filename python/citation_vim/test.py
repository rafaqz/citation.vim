# -*- coding: utf-8 -*-

"""
Tests your citation database in the console

Example *nix style commands:
python test.py /your/bibtext/file bibtex key
python test.py /your/zotero/path zotero key "searchstring" 4
"""

import sys
import os.path
import re
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, module_path)
from citation_vim.builder import Builder
from citation_vim.context import Context

def get_console_context(context):
    context.bibtex_file = sys.argv[1]
    context.zotero_path = sys.argv[1]
    context.mode = sys.argv[2]
    context.source_field = sys.argv[3] 
    if context.mode == 'zotero':
        context.searchkeys = sys.argv[4].split()
        context.zotero_version = int(sys.argv[5])
    return context

def set_default_context(context):
    context.cache_path = ""
    context.collection = ''
    context.source = 'citation'
    context.key_format = "{author}{date}{Title}"

    context.key_title_banned_regex = re.compile("\\b(a|an|the|some|from|on|in|to|of|" "do|with|der|die|das|ein|eine|einer|eines|einem|einen|" "un|une|la|le|l|el|las|los|al|uno|una|unos|unas|de|des|del|d)\\W")
    context.key_clean_regex = re.compile("[^A-Za-z0-9\!\$\&\*\+\-\.\/\:\;\<\>\?\[\]\^\_\`\|]+")
    context.desc_format = u"{} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}"
    context.desc_fields = ["abstract", "author", "collections", "date", "doi", 
                           "file", "isbn", "issue", "key", "language", "notes", "pages", 
                           "publication", "publisher", "tags", "title", "type", "url", "volume"]
    context.et_al_limit = 5
    context.wrap_chars = "[]"
    context.zotero_attachment_path = "~/Zotero/library/"
    context.cache = False
    return context

def print_output(output):
    for field, desc, file, combined in output:
        print("\nField: ")
        print(field)
        print("\nDescription: ")
        print(desc)
        print("\nFile: ")
        print(file)
        print("\nCombined: ")
        print(combined)

context = Context()
context = get_console_context(context)
context = set_default_context(context)
output = Builder(context).build_source()
print_output(output)
