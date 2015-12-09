# -*- coding: utf-8 -*-

import os.path
import string
from pybtex.database.input import bibtex

class unite_bibtex(object):

    class Bibentry(object):
         def __init__(self, 
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

            self.__dict__.update(locals())
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
        combined = u"\n[{}]\nKey: {}\nTitle: {}\nAuthor(s): {}\nMonth: {}\nYear: {}\nAbstract: {}\nJournal: {}\nVolume: {}\nPages: {}\nPublisher: {}\nLang: {}\nFile(s): {}\nURL:{}\nDOI:{}\nISBN:{}\nAnnotation: {}".format(
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
            if sys.version_info[0] == 2:
                authors = [unicode(au) for au in persons]
            elif sys.version_info[0] == 3:
                authors = [str(au) for au in persons]
        except KeyError:
            authors = [""]
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
                if field in ['author','key','combined']:
                    if field == 'author': 
                        try:
                            entry.persons[u'author']
                        except:
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
    def description(entry, field, desc_fields, desc_format):
        eval_fields = []
        source_field = ""
        if not field in desc_fields + ["combined","file"]:
            source_field = "[" + eval("entry." + field) + "]"
        for desc_field in desc_fields:
            try:
                eval("entry." + desc_field)
            except AttributeError:
                return 'Erro at "{}" field of g:unite_bibtex_description_fields. Check your vimrc.'.format(desc_field)
            eval_fields = eval_fields + [eval("entry." + desc_field)]
        if field in desc_fields:
            index = desc_fields.index(field)
            f = eval_fields[index]
            eval_fields[index] = "[" + f + "]"
        return desc_format.format(*eval_fields) + " " + source_field


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
            desc = unite_bibtex.description(entry, field, desc_fields, desc_format)
            output.append([eval("entry." + field), desc])
        return output

if __name__ == '__main__':
    import sys
    bibpaths = sys.argv[1:]
    entries = unite_bibtex.get_entries(bibpaths,"combined")
    for k, v in entries.items():
        print(u"{}:{}".format(k, v.combined))
