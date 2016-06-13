# -*- coding:utf-8 -*-

class Item(object):

    """
    Intermediary object between bibtex/zotero and unite source output.
    """

    def combine(self):
        self.combined = u"[{}]\\nKey: {}\\nTitle: {}\\nAuthor(s): {}\\nDate: {}\\nTags: {}\\nCollections: {}\\nAbstract: {}\\nPublication: {}\\nIssue: {}\\nVolume: {}\\nPages: {}\\nPublisher: {}\\nLang: {}\\nFile(s): {}\\nURL:{}\\nDOI:{}\\nISBN:{}\\nNotes: {}".format(
            self.type,
            self.key,
            self.title,
            self.author, 
            self.date,
            self.tags,
            ', '.join(self.collections),
            self.abstract,
            self.publication, 
            self.issue, 
            self.volume, 
            self.pages, 
            self.publisher, 
            self.language, 
            self.file, 
            self.url, 
            self.doi, 
            self.isbn, 
            self.notes
         ).replace('"',"'")
