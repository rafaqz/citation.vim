#-*- coding:utf-8 -*-

class Item(object):

    """
    Intermediary object between bibtex/zotero and unite source output.
    """

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

    def describe(self, source_field, desc_fields, desc_format):
        desc_strings = []
        source_string = ""
        for desc_field in desc_fields:
            try:
                getattr(self, desc_field)
            except AttributeError:
                return 'Error at "{}" field of g:unite_bibtex_description_fields. Check your vimrc.'.format(desc_field)
            desc_strings = desc_strings + [getattr(self, desc_field)]

        if source_field in desc_fields:
            index = desc_fields.index(source_field)
            f = desc_strings[index]
            desc_strings[index] = "【" + f + "】"
        else:
            if not source_field in ["combined","file"]:
                source_string = " 【" + getattr(self, source_field) + "】"

        return desc_format.format(*desc_strings) + source_field

