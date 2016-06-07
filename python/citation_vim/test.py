#-*- coding:utf-8 -*-

import sys
import os.path
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, module_path)
from citation_vim.citation import Citation

# source = "citation"
context = Citation.Context()
context.source = "fulltext"
context.source_field = "key"
context.bibtex_file = sys.argv[1]
context.zotero_path = sys.argv[1]
context.mode = sys.argv[2]
context.cache_path = sys.argv[3]
context.desc_format = u"{}∶ {} \"{}\" -{}- ({})"
context.desc_fields = ["type", "key", "title", "author", "date"]
context.wrap_chars = "[]"
builder = Citation.Builder(context)
items = builder.build_list()
for field, desc in items:
    print("\nField: ")
    print(field)
    print("\nDescription: ")
    print(desc)
