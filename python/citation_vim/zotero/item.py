# -*- coding: utf-8 -*-

class zoteroItem(object):

    """Represents a single zotero item."""

    def __init__(self, init=None):

        """
        Constructor.

        Keyword arguments:
        init -- An `int` with the item id . (default=None)
        """

        self.title = ""
        self.collections = []
        self.publication = ""
        self.publisher = ""
        self.authors = []
        self.notes = []
        self.tags = []
        self.issue = ""
        self.pages = ""
        self.doi = ""
        self.isbn = ""
        self.abstract = ""
        self.language = ""
        self.volume = ""
        self.fulltext = []
        self.date = ""
        self.url = ""
        self.key = ""
        if isinstance(init, int):
            self.id = init
        else:
            self.id = ""
