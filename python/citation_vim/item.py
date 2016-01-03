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

    def describe(self, field, desc_fields, desc_format):
        eval_fields = []
        source_field = ""
        if not field in desc_fields + ["combined","file"]:
            source_field = "【" + eval("self." + field) + "】"
        for desc_field in desc_fields:
            try:
                eval("self." + desc_field)
            except AttributeError:
                return 'Erro at "{}" field of g:unite_bibtex_description_fields. Check your vimrc.'.format(desc_field)
            eval_fields = eval_fields + [eval("self." + desc_field)]
        if field in desc_fields:
            index = desc_fields.index(field)
            f = eval_fields[index]
            eval_fields[index] = "【" + f + "】"
        return desc_format.format(*eval_fields) + " " + source_field

