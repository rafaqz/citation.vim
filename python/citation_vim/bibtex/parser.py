# -*- coding: utf-8 -*-
import os.path
import sys
from pybtex.database.input import bibtex
from citation_vim.item import Item
from citation_vim.utils import check_path, raiseError

class bibtexParser(object):

    def __init__(self, context):
        self.context = context
        self.bibtex_file = check_path(self.context.bibtex_file)
        self.et_al_limit = context.et_al_limit

    def load(self):

        """
        Returns:
        A bibtex file as an array of Items.
        """

        items = []
        try:
            bib_data = self._read_file(self.bibtex_file)
        except Exception as e:
            raiseError(u"Failed to read {}".format(self.bibtex_file, '\r', u"Message: {}".format(str(e))))

        for key in bib_data.entries:
            bib_entry = bib_data.entries[key]

            item = Item()
            item.abstract  = self.get_field(bib_entry, "abstract")
            item.author    = self.format_author(bib_entry)
            item.collections  = []
            item.date      = self.get_field(bib_entry, "year")
            item.doi       = self.get_field(bib_entry, "doi")
            item.file      = self.format_file(bib_entry)
            item.isbn      = self.get_field(bib_entry, "isbn")
            item.publication = self.get_field(bib_entry, "journal")
            item.key       = key
            item.language  = self.get_field(bib_entry, "language")
            item.issue     = self.get_field(bib_entry, "number")
            item.notes     = self.get_field(bib_entry, "annote")
            item.pages     = self.get_field(bib_entry, "pages")
            item.publisher = self.get_field(bib_entry, "publisher")
            item.tags      = self.get_field(bib_entry, "keyword")
            item.title     = self.get_field(bib_entry, "title")
            item.type      = bib_entry.type
            item.url       = self.format_url(bib_entry)
            item.volume    = self.get_field(bib_entry, "volume")
            item.combine()
            items.append(item)
        return items

    def _read_file(self, filename):
        parser = bibtex.Parser()
        return parser.parse_file(filename)

    def strip_chars(self, string):
        return string.replace("{","").replace("}","")

    def get_field(self, entry, field):
        output = entry.fields[field] if field in entry.fields else ""
        output = self.strip_chars(output)
        return output

    def format_author(self, entry):

        """
        Returns:
        A pretty representation of the author.
        """

        try:
            persons = entry.persons[u"author"]
            if sys.version_info[0] == 2:
                authors = [unicode(au).split(",") for au in persons]
            elif sys.version_info[0] == 3:
                authors = [str(au).split(",") for au in persons]
        except KeyError:
            authors = []

        if authors == []:
            return ""
        if len(authors) > int(self.et_al_limit):
            return u"%s et al." % authors[0][0]
        if len(authors) > 2:
            auth_string = u""
            for author in authors[:-1]:
                auth_string += author[0] + ', '
            return auth_string + u"& " + authors[-1][0]
        if len(authors) == 2:
            return authors[0][0] + u" & " + authors[1][0]
        return ', '.join(authors[0])

    def format_file(self, entry):
        output = ""
        if u"file" in entry.fields:
            for file in entry.fields[u"file"].split(";"):
                details = file.split(":")
                if 2 < len(details) and details[2] == "application/pdf":
                    output = details[1]
                    break
        return output

    def format_url(self, entry):
        output = ""
        if u"file" in entry.fields:
            for file in entry.fields[u"file"].split(";"):
                details = file.split(":")
                if 2 < len(details) and details[2] != "application/pdf":
                    output = details[1]
                    break
        return output

    def format_tags(entry):
        output = ""
        if u"keywords" in entry.fields:
            output = ", ".join(entry.fields[u"keywords"])
        return output

