#-*- coding:utf-8 -*-

import sys
import os.path
module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
sys.path.insert(0, module_path)
from citation_vim.connect import Citation

field = "title"
file_path = sys.argv[1]
file_format = sys.argv[2]
cache_path = '~/.vim/temp_dirs/'
desc_format = u"{}∶ {} \"{}\" -{}- ({})"
desc_fields = ["type", "key", "title", "author", "date"]
wrap_chars = "[]"
items = Citation.get_entries(field, file_path, cache_path, file_format, desc_fields, desc_format, wrap_chars)
for field, desc in items:
    print(field)
    print(desc)
