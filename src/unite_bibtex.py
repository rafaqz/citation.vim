# -*- coding: utf-8 -*-

import os.path
from pybtex.database.input import bibtex
from pbtex import errors


class unite_bibtex(object):
    """
    Name space for unite_bibtex.vim
    (not to pollute global name space)
    """

    def _read_file(self, filename):
        errors.enable_strict_mode()
        parser = bibtex.Parser()
        return parser.parse_file(filename)

    def _check_path(self, path):
        path = os.path.abspath(os.path.expanduser(path))
        if not os.path.exists(path):
            raise RuntimeError("file:%s not found" % path)
        return path

    def entry_to_str(self, entry):
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

    def get_entries(self, bibpath_list):
        entries = {}
        for bibpath in bibpath_list:
            path = self._check_path(bibpath)
            bibdata = self._read_file(path)
            for key in bibdata.entries:
                try:
                    k = key.encode("utf-8")
                except:
                    print("Cannot encode bibtex key, skip: {}".format(k))
                    continue
                entries[k] = self.entry_to_str(bibdata.entries[key]).encode("utf-8")
        return entries
