# -*- coding: utf-8 -*-

class zoteroItem(object):

    """Represents a single zotero item."""

    def __init__(self, _id):

        """
        Constructor.

        Keyword arguments:
        _id -- An `int` with the item id.
        """

        self.id = _id
        self.title = ""
        self.collections = []
        self.publicationTitle = ""
        self.publisher = ""
        self.authors = []
        self.notes = []
        self.tags = []
        self.issue = ""
        self.pages = ""
        self.DOI = ""
        self.ISBN = ""
        self.abstractNote = ""
        self.language = ""
        self.volume = ""
        self.fulltext = []
        self.date = ""
        self.url = ""
        self.key = ""
