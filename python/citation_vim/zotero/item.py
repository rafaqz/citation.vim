#-*- coding:utf-8 -*-

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

    def format_author(self):

        """
        Returns:
        A pretty representation of the author.
        """

        if self.authors == []:
            return ""
        if len(self.authors) > 5:
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
        Returns:
        Comma separated tags.
        """

        return u", ".join(self.tags)

    def format_notes(self):

        """
        Returns:
        Linebreak separated notes.
        """

        return u"\n\n".join(self.notes)

    def format_fulltext(self):

        """
        Returns:
        The first file.
        """

        if self.fulltext == []:
            return ""
        else:
            return self.fulltext[0]
