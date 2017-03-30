# -*- coding: utf-8 -*-

import re

class ZoteroItem(object):

    """Represents a single zotero item."""

    def __init__(self, _id):

        """
        Constructor.

        Keyword arguments:
        _id -- An `int` with the item id.
        """

        self.id = _id
        self.abstractNote = ""
        self.attachments = []
        self.authors = []
        self.collections = []
        self.date = ""
        self.DOI = ""
        self.ISBN = ""
        self.issue = ""
        self.key = ""
        self.language = ""
        self.notes = []
        self.pages = ""
        self.publicationTitle = ""
        self.publisher = ""
        self.tags = []
        self.title = ""
        self.url = ""
        self.volume = ""
        self.zotero_key = ""

    def format_first_author(self):
        """
        Returns: The first authors surname, if one exists.
        """
        if self.authors == []:
            return "" 
        return self.authors[0][0] 

    def format_author(self, et_al_limit = 2):
        """
        Returns: A pretty representation of the author.
        """
        if self.authors == []:
            return ""
        if len(self.authors) > et_al_limit:
            return u"%s et al." % self.authors[0][0]
        if len(self.authors) > 2:
            auth_string = u""
            for author in self.authors[:-1]:
                auth_string += author[0] + ', '
            return auth_string + u"& " + self.authors[-1][0]
        if len(self.authors) == 2:
            return self.authors[0][0] + u" & " + self.authors[1][0]
        return ', '.join(self.authors[0])

    def format_tags(self):
        """
        Returns: Comma separated tags.
        """
        return u", ".join(self.tags)

    def format_notes(self):
        """
        Returns: Linebreak separated notes.
        """
        return u"\n\n".join(self.notes)

    def format_attachment(self):
        """
        Returns: The first file.
        """
        if self.attachments == []:
            return ""
        return self.attachments[0]

    def format_date(self):
        """
        Returns: The year or special string.
        """
        # Some dates are treated as special and are not parsed into a year
        # representation
        special_dates = u"in press", u"submitted", u"in preparation", \
            u"unpublished"
        for specialdate in special_dates:
            if specialdate in self.date.lower():
                return specialdate

        date = ""
        for split in re.split(' |-|/', self.date):
            if len(split) == 4 and split.isdigit():
                date = split
                break
        return date
