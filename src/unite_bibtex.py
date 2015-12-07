# -*- coding: utf-8 -*-

import os.path
from pybtex.database.input import bibtex

def clean(entry, field):
    ufield = "u{}".format(field)
    output = entry.fields[ufield] if ufield in entry.fields else ""
    return output.encode("utf-8")

class Bibentry(object):
    # The class "constructor" - It's actually an initializer 
    def __init__(self, 
                abstract,
                author,
                desc,
                doi,
                filename,
                isbn,
                journal,
                key,
                language,
                publisher,
                title,
                url,
                year):

        self.desc = desc
        self.filename = filename
        self.url = url

class unite_bibtex(object):
    """
    Name space for unite_bibtex.vim
    (not to pollute global name space)
    """

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
    def entry_to_str(entry):
        try:
            persons = entry.persons[u'author']
            authors = [unicode(au) for au in persons]
        except:
            authors = [u'unknown']
        title = entry.fields[u"title"] if u"title" in entry.fields else ""
        journal = entry.fields[u"journal"] if u"journal" in entry.fields else ""
        year = entry.fields[u"year"] if u"year" in entry.fields else ""
        filename = "+FILE" if u"file" in entry.fields else ""
        url = "+URL" if u"url" in entry.fields else ""
        desc = u" %s %s %s(%s), %s, %s" % (",".join(authors), title, journal, year, url, filename)
        return desc.replace("'", "").replace("\\", "")

    @staticmethod
    def get_entries(bibpaths):
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
                    k = key.encode("utf-8")
                except:
                    print("Cannot encode bibtex key, skip: {}".format(k))
                    continue
                entry = bibdata.entries[key]
                desc = k + unite_bibtex.entry_to_str(entry)
                filename = entry.fields[u"file"].split(':')[1] if u"file" in entry.fields else ""
                entries[k] = Bibentry(
                    clean(entry, "abstract"),
                    clean(entry, "author"),
                    clean(entry, "doi"),
                    desc.encode("utf-8"),
                    filename.encode("utf-8"),
                    clean(entry, "isbn"),
                    clean(entry, "journal"),
                    k,
                    clean(entry, "language"),
                    clean(entry, "publisher"),
                    clean(entry, "title"),
                    clean(entry, "url"),
                    clean(entry, "year"))
        return entries

if __name__ == '__main__':
    import sys
    bibpaths = sys.argv[1:]
    entries = unite_bibtex.get_entries(bibpaths)
    for k, v in entries.items():
        print("{}:{}".format(k, v))
