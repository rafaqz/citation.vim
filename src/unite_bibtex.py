# -*- coding: utf-8 -*-

import os.path
import string
from pybtex.database.input import bibtex

class unite_bibtex(object):
    """
    Name space for unite_bibtex.vim
    (not to pollute global name space)
    """
    class Bibentry(object):
         def __init__(
                    self, 
                    abstract,
                    annote,
                    author,
                    doi,
                    file,
                    isbn,
                    journal,
                    key,
                    language,
                    month,
                    pages,
                    publisher,
                    shorttitle,
                    title,
                    type,
                    url,
                    volume,
                    year,
                    ):

            self.abstract = abstract 
            self.annote = annote 
            self.author = author 
            self.doi = doi 
            self.file = file
            self.isbn = isbn 
            self.journal = journal 
            self.key = key 
            self.language = language 
            self.month = month 
            self.pages = pages 
            self.publisher = publisher 
            self.title = title 
            self.type = type 
            self.shorttitle = shorttitle 
            self.url = url 
            self.volume = volume
            self.year = year
            self.combined = unite_bibtex.combine(self)

    @staticmethod
    def _read_file(filename):
        parser = bibtex.Parser()
        return parser.parse_file(filename)

    @staticmethod
    def _check_path(path):
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(path):
            raise RuntimeError("file:%s not found" % path)
        return path

    @staticmethod
    def strip_chars(string):
        return string.replace("{","").replace("}","")

    @staticmethod
    def clean(entry, field):
        output = entry.fields[field] if field in entry.fields else ""
        output = unite_bibtex.strip_chars(output)
        return output

    @staticmethod
    def combine(entry):
        combined = u"\n  [{}]\n  Key: {}\n  Title: {}\n  Author(s): {}\n  Month: {}\n  Year: {}\n  Abstract: {}\n  Journal: {}\n  Volume: {}\n  Pages: {}\n  Publisher: {}\n  Lang: {}\n  File(s): {}\n  URL:  {}\n  DOI:  {}\n  ISBN:  {}\n  Annotation: {}".format(
                entry.type,
                entry.key,
                entry.title,
                entry.author, 
                entry.month,
                entry.year,
                entry.abstract,
                entry.journal, 
                entry.volume, 
                entry.pages, 
                entry.publisher, 
                entry.language, 
                entry.file, 
                entry.url, 
                entry.doi, 
                entry.isbn, 
                entry.annote, 
                )
        return combined

    @staticmethod
    def authors(entry):
        try:
            persons = entry.persons[u"author"]
            authors = [str(au) for au in persons]
        except KeyError:
            authors = [u"unknown"]
        authors = unite_bibtex.strip_chars("; ".join(authors))
        return authors

    @staticmethod
    def file(entry):
        output = ""
        if u"file" in entry.fields: 
            output = entry.fields[u"file"].split(":")[1]
        return output

    @staticmethod
    def get_entries(bibpaths,field):
        entries = {}
        for bibpath in bibpaths:
            try:
                path = unite_bibtex._check_path(bibpath)
                bibdata = unite_bibtex._read_file(path)
            except Exception as e:
                print("Failed to read {}".format(bibpath))
                print("Message: {}".format(str(e)))
                continue
            for key in bibdata.entries:
                try:
                    k = key
                except:
                    print("Cannot encode bibtex key, skip: {}".format(k))
                    continue
                entry = bibdata.entries[key]
                if field in ['url','author','key','combined']:
                    if field == 'author' and not entry.persons:
                         continue
                else:
                     if not field in entry.fields:
                         continue

                entries[k] = unite_bibtex.Bibentry(
                    unite_bibtex.clean(entry, "abstract"),
                    unite_bibtex.clean(entry, "annote"),
                    unite_bibtex.authors(entry),
                    unite_bibtex.clean(entry, "doi"),
                    unite_bibtex.file(entry),
                    unite_bibtex.clean(entry, "isbn"),
                    unite_bibtex.clean(entry, "journal"),
                    key,
                    unite_bibtex.clean(entry, "language"),
                    unite_bibtex.clean(entry, "month"),
                    unite_bibtex.clean(entry, "pages"),
                    unite_bibtex.clean(entry, "publisher"),
                    unite_bibtex.clean(entry, "shorttitle"),
                    unite_bibtex.clean(entry, "title"),
                    entry.type,
                    unite_bibtex.clean(entry, "url"),
                    unite_bibtex.clean(entry, "volume"),
                    unite_bibtex.clean(entry, "year"))
        return entries

    @staticmethod
    def description(entry, desc_fields, desc_format):
        eval_fields = []
        for field in desc_fields:
            try:
                eval("entry." + field)
            except AttributeError:
                return 'Erro at "{}" field of g:unite_bibtex_description_fields. Check your vimrc.'.format(field)
            eval_fields = eval_fields + [str(eval("entry." + field))]
        return desc_format.format(*eval_fields)

    @staticmethod
    def connect():
        import vim
        bibpaths = vim.eval("g:unite_bibtex_bib_files")
        desc_format = vim.eval("g:unite_bibtex_description_format")
        desc_fields = vim.eval("g:unite_bibtex_description_fields")
        field = vim.eval("a:field")
        entries = unite_bibtex.get_entries(bibpaths, field)
        output = []
        for key, entry in entries.items():
            desc = unite_bibtex.description(entry, desc_fields, desc_format)
            output.append([eval("entry." + field), desc])
        return output

if __name__ == '__main__':
    import sys
    bibpaths = sys.argv[1:]
    entries = unite_bibtex.get_entries(bibpaths,"combined")
    for k, v in entries.items():
        print(u"{}:{}".format(k, v.combined))
