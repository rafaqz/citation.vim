# -*- coding: utf-8 -*-

import collections
from citation_vim.utils import compat_str, is_current

class Item(object):

    """
    Intermediary object between bibtex/zotero and unite source output.
    """

    def combine(self):
        pairs = collections.OrderedDict([
            ('Key', self.key),
            ('Title', self.title),
            ('Author(s)', self.author),
            ('Date', self.date),
            ('Tags', self.tags),
            ('Collections', ', '.join(self.collections)),
            ('Publication', self.publication),
            ('Issue', self.issue),
            ('Volume', self.volume),
            ('Pages', self.pages),
            ('Publisher', self.publisher),
            ('Language', self.language),
            ('Abstract', self.abstract),
            ('Notes', self.notes),
            ('File(s)', self.file),
            ('URL', self.url),
            ('DOI', self.doi),
            ('ISBN', self.isbn)
        ])
        self.combined = u"Available citation information:\n"
        for key, value in pairs.items():
            if value:
                self.combined += "  " + key + " : " + compat_str(value) + "\n"
