# -*- coding: utf-8 -*-

import os.path
import string
import json
import sys

class unite_bibtex(object):

    class Zotero(object):

        """
        Returns: 
        A zotero database as an array of Items.
        """

        def load(self, field, file_path):
            import libzotero

            if not libzotero.valid_location(file_path):
                print("{} is not a valid zotero path".format(file_path))
                return []

            self.load_citekeys(file_path)

            try:
                zotero = libzotero.LibZotero(file_path)
                data = zotero.load()
            except Exception as e:
                print("Failed to read {}".format(file_path))
                print("Message: {}".format(str(e)))

            items = []
            for entry_id, entry in data:

                item = unite_bibtex.Item()
                item.abstract  = entry.abstract,
                item.author    = entry.format_author()
                item.date      = entry.date
                item.doi       = entry.doi
                item.file      = entry.fulltext
                item.isbn      = entry.isbn
                item.journal   = entry.publication
                item.key       = self.format_key(entry.id, entry.key)
                item.language  = entry.language
                item.issue     = entry.issue
                item.notes     = entry.format_notes()
                item.pages     = entry.pages
                item.publisher = entry.publisher
                item.tags      = entry.format_tags()
                item.title     = entry.title
                item.type      = entry.type
                item.url       = entry.url
                item.volume    = entry.volume
                item.combine()
                
                items.append(item)
            return items


        def format_key(self, id, key):
            if id in self.citekeys:
                return self.citekeys[id]
            else:
                return key

        def load_citekeys(self, file_path):
            """
            Loads better-bibtex citekeys if they exist.
            """
            self.citekeys = {}
            bb_path = os.path.join(file_path, 'better-bibtex/db.json')
            if os.path.exists(bb_path):
                with open(bb_path) as bb:    
                    bb_json = json.load(bb)
                for item in bb_json['collections'][0]['data']:
                    self.citekeys[item['itemID']] = item['citekey']

    class Bibtex(object):

        def load(self, field, file_path):

            """
            Returns: 
            A bibtex file as an array of Items.
            """
            items = []
            try:
                path = self._check_path(file_path)
                data = self._read_file(path)
            except Exception as e:
                print("Failed to read {}".format(file_path))
                print("Message: {}".format(str(e)))
                return []

            for key in data.entries:
                entry = data.entries[key]
                if not field in ['author','key','combined'] and not field in entry.fields:
                    continue
                if field == 'author': 
                    try:
                        entry.persons[u'author']
                    except:
                        continue
                print(entry.type)

                item = unite_bibtex.Item()
                item.abstract  = self.get_field(entry, "abstract")
                item.author    = self.format_author(entry)
                item.date      = self.get_field(entry, "month") + self.get_field(entry, "year")
                item.doi       = self.get_field(entry, "doi")
                item.file      = self.format_file(entry)
                item.isbn      = self.get_field(entry, "isbn")
                item.journal   = self.get_field(entry, "journal")
                item.key       = key,
                item.language  = self.get_field(entry, "language")
                item.issue     = self.get_field(entry, "number")
                item.notes     = self.get_field(entry, "annote")
                item.pages     = self.get_field(entry, "pages")
                item.publisher = self.get_field(entry, "publisher")
                item.tags      = self.get_field(entry, "keyword")
                item.title     = self.get_field(entry, "title")
                item.type      = entry.type,
                item.url       = self.get_field(entry, "url")
                item.volume    = self.get_field(entry, "volume")
                item.combine()

                items.append(item)
            return items

        def _read_file(self, filename):
            from pybtex.database.input import bibtex
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

    class Item(object):

        def combine(self):
            self.combined = u"\n[{}]\nKey: {}\nTitle: {}\nAuthor(s): {}\nDate: {}\nAbstract: {}\nJournal: {}\nIssue: {}\nVolume: {}\nPages: {}\nPublisher: {}\nLang: {}\nFile(s): {}\nURL:{}\nDOI:{}\nISBN:{}\nAnnotation: {}".format(
                self.type,
                self.key,
                self.title,
                self.author, 
                self.date,
                self.abstract,
                self.journal, 
                self.issue, 
                self.volume, 
                self.pages, 
                self.publisher, 
                self.language, 
                self.file, 
                self.url, 
                self.doi, 
                self.isbn, 
                self.notes)

        def describe(self, field, desc_fields, desc_format):
            eval_fields = []
            source_field = ""
            if not field in desc_fields + ["combined","file"]:
                source_field = "【" + eval("self." + field) + "】"
            for desc_field in desc_fields:
                try:
                    eval("self." + desc_field)
                except AttributeError:
                    return 'Erro at "{}" field of g:unite_bibtex_description_fields. Check your vimrc.'.format(desc_field)
                eval_fields = eval_fields + [eval("self." + desc_field)]
            if field in desc_fields:
                index = desc_fields.index(field)
                f = eval_fields[index]
                eval_fields[index] = "【" + f + "】"
            return desc_format.format(*eval_fields) + " " + source_field

    @staticmethod
    def get_entries(field, file_path, file_format):
        if file_format == "bibtex":
            citations = unite_bibtex.Bibtex()
        elif file_format == "zotero":
            citations = unite_bibtex.Zotero()
        return citations.load(field, file_path)

    @staticmethod
    def connect():
        import vim
        file_format = vim.eval("g:unite_bibtex_file_format")
        file_path   = vim.eval("g:unite_bibtex_file_path")
        desc_format = vim.eval("g:unite_bibtex_description_format")
        desc_fields = vim.eval("g:unite_bibtex_description_fields")
        field       = vim.eval("a:field")
        script_folder = vim.eval('s:script_folder_path')
        script_folder = os.path.join(script_folder, '../../../src') 
        sys.path.insert( 0, script_folder)

        entries = unite_bibtex.get_entries("title", file_path, file_format)
        output = []
        for entry in entries:
            desc = entry.describe(field, desc_fields, desc_format)
            output.append([eval("entry." + field), desc])
        return output

