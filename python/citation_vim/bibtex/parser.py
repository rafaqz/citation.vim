# -*- coding: utf-8 -*-
import os.path
import sys
from pybtex.database.input import bibtex
from citation_vim.item import Item

class bibtexParser(object):

    def load(self, source_field, file_path):

        """
        Returns: 
        A bibtex file as an array of Items.
        """
        items = []
        try:
            bib_path = self._check_path(file_path)
            bib_data = self._read_file(bib_path)
        except Exception as e:
            print("Failed to read {}".format(file_path))
            print("Message: {}".format(str(e)))
            return []

        for key in bib_data.entries:
            bib_entry = bib_data.entries[key]
            if not source_field in ['author','key','combined'] and not source_field in bib_entry.fields:
                continue
            if source_field == 'author': 
                try:
                    bib_entry.persons[u'author']
                except:
                    continue

            item = Item()
            item.abstract  = self.get_field(bib_entry, "abstract")
            item.author    = self.format_author(bib_entry)
            item.date      = self.get_field(bib_entry, "month") + self.get_field(bib_entry, "year")
            item.doi       = self.get_field(bib_entry, "doi")
            item.file      = self.format_file(bib_entry)
            item.isbn      = self.get_field(bib_entry, "isbn")
            item.journal   = self.get_field(bib_entry, "journal")
            item.key       = key
            item.language  = self.get_field(bib_entry, "language")
            item.issue     = self.get_field(bib_entry, "number")
            item.notes     = self.get_field(bib_entry, "annote")
            item.pages     = self.get_field(bib_entry, "pages")
            item.publisher = self.get_field(bib_entry, "publisher")
            item.tags      = self.get_field(bib_entry, "keyword")
            item.title     = self.get_field(bib_entry, "title")
            item.type      = bib_entry.type
            item.url       = self.get_field(bib_entry, "url")
            item.volume    = self.get_field(bib_entry, "volume")
            item.combine()
            if not getattr(item, source_field) == "":
                items.append(item)
        return items

    def _read_file(self, filename):
        parser = bibtex.Parser()
        return parser.parse_file(filename)

    def _check_path(self, path):
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(path):
            raise RuntimeError("file:%s not found" % path)
        return path

    def strip_chars(self, string):
        return string.replace("{","").replace("}","")

    def get_field(self, entry, field):
        output = entry.fields[field] if field in entry.fields else ""
        output = self.strip_chars(output)
        return output

    def format_author(self, entry):
        try:
            persons = entry.persons[u"author"]
            if sys.version_info[0] == 2:
                authors = [unicode(au) for au in persons]
            elif sys.version_info[0] == 3:
                authors = [str(au) for au in persons]
        except KeyError:
            authors = [""]
        authors = self.strip_chars("; ".join(authors))
        return authors

    def format_file(self, entry):
        output = ""
        if u"file" in entry.fields: 
            output = entry.fields[u"file"].split(":")[1]
        return output

    def format_tags(entry):
        output = ""
        if u"keywords" in entry.fields: 
            output = ", ".join(entry.fields[u"keywords"])
        return output

