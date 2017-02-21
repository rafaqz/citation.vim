# -*- coding: utf-8 -*-

"""
Tests your citation database in the console

Example *nix style commands:
python test.py /your/bibtext/file bibtex key
python test.py /your/zotero/path zotero key "searchstring" 4
"""

import sys
import os.path
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, module_path)
from citation_vim.builder import Builder
from citation_vim.context import Context

def get_console_context():
    context = Context()
    context.bibtex_file = sys.argv[1]
    context.zotero_path = sys.argv[1]
    context.mode = sys.argv[2]
    context.source_field = sys.argv[3] 
    if context.mode == 'zotero':
        context.searchkeys = sys.argv[4].split()
        context.zotero_version = int(sys.argv[5])

    context.cache_path = ""
    context.collection = ''
    context.source = 'citation'
    context.key_format = "{author}{date}{Title}"
    context.desc_format = u"{}∶ {} \"{}\" -{}- ({})"
    context.desc_fields = ["type", "key", "title", "author", "date"]
    context.et_al_limit = 5
    context.wrap_chars = "[]"
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

output = Builder(get_console_context()).build_source()
print_output(output)

