# -*- coding: utf-8 -*-

import os.path
from pybtex.database.input import bibtex


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
        desc = u"%s %s %s(%s)" % (",".join(authors), title, journal, year)
        return desc.replace("'", "").replace("\\", "")

    @staticmethod
    def get_entries(bibpath_list):
        entries = {}
        for bibpath in bibpath_list:
            try:
                path = unite_bibtex._check_path(bibpath)
                bibdata = unite_bibtex._read_file(path)
            except Exception as e:
                print("Fail to read {}".format(bibpath))
                print("Message: {}".format(str(e)))
                continue
            for key in bibdata.entries:
                try:
                    k = key.encode("utf-8")
                except:
                    print("Cannot encode bibtex key, skip: {}".format(k))
                    continue
                entries[k] = unite_bibtex.entry_to_str(bibdata.entries[key]).encode("utf-8")
        return entries

if __name__ == '__main__':
    import sys
    bibpath_list = sys.argv[1:]
    entries = unite_bibtex.get_entries(bibpath_list)
    for k, v in entries.items():
        print("{}:{}".format(k, v))
