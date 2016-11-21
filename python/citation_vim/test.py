# -*- coding:utf-8 -*-

import sys
import os.path
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, module_path)
from citation_vim.citation import Citation, Context, Builder

context = Context()
context.bibtex_file = sys.argv[1]
context.zotero_path = sys.argv[1]
context.collection = ''
context.mode = sys.argv[2]
context.cache_path = sys.argv[3]
context.source = sys.argv[4]
context.source_field = sys.argv[5] 
context.searchkeys = sys.argv[6].split()
context.desc_format = u"{}∶ {} \"{}\" -{}- ({})"
context.et_al_limit = 5
context.desc_fields = ["type", "key", "title", "author", "date"]
context.wrap_chars = "[]"
builder = Builder(context, cache = False)
items = builder.build_list()
for field, desc, file, combined in items:
    print("\nField: ")
    print(field)
    print("\nDescription: ")
    print(desc)
    print("\nFile: ")
    print(file)
    print("\nCombined: ")
    print(combined)
