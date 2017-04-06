# -*- coding: utf-8 -*-

import collections
from citation_vim.utils import compat_str, is_current

class Item(object):

    """
    Intermediary object between a bibtex/zotero item and a row in unite source output.
    """

    def __init__(self):
        self.zotero_key = ""


    def combine(self):
        pairs = collections.OrderedDict([
            ('Key', self.key),
            ('Title', self.title),
            ('Type', self.type),
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
            ('ISBN', self.isbn),
            ('Zotero key', self.zotero_key)
        ])
        self.combined = u"Available citation fields:\n"
        for key, value in pairs.items():
            if value:
                self.combined += "  " + key + " : " + compat_str(value) + "\n"

    def describe(self, context):
        """
        Returns visible text descriptions for unite, from user selected fields.
        """
        self.context = context
        description_values = self.get_description_values()
        return self.describe_with_source_field(description_values)

    def get_description_values(self):
        description_fields = self.context.desc_fields
        description_values = []
        for description_field in description_fields:
            if hasattr(self, description_field):
                description_values.append(getattr(self, description_field))
            else:
                description_values.append("")
        return description_values

    def describe_with_source_field(self, description_values):
        """
        Returns description with added/replaced wrapped source field
        """
        description_fields = self.context.desc_fields
        description_format = self.context.desc_format
        source_field = self.context.source_field
        wrapper = self.context.wrap_chars
        if hasattr(self, source_field):
            source_value = getattr(self, source_field)
        else: 
            source_value = ""
        wrapped_source = self.wrap_string(source_value, wrapper)
        if source_field in description_fields:
            source_index = description_fields.index(source_field)
            description_values[source_index] = wrapped_source
        elif not source_field in ["combined"]:
            description_format += wrapped_source
        return description_format.format(*description_values)

    def wrap_string(self, string, wrapper):
        return u'%s%s%s' % (wrapper[0], string, wrapper[1])
