from unite_bibtex import unite_bibtex as unite_bibtex
import sys

file_path = sys.argv[1]
file_format = sys.argv[2]
desc_format = "{}∶ {} ˝{}˝ ☆{}☆ ₍{}₎"
desc_fields = ["type", "key", "title", "author", "date"]
entries = unite_bibtex.get_entries("title", file_path, file_format)
for entry in entries:
    desc = entry.describe("title", desc_fields, desc_format)
    print(u"{}\n{}\n".format(entry.combined, desc))
