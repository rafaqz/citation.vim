# -*- coding: utf-8 -*-

import collections
from citation_vim.utils import compat_str, is_current, strip_braces

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
        desc_values = self.get_description_values()
        return self.describe_with_source_field(desc_values)

    def get_description_values(self):
        desc_fields = self.context['desc_fields']
        desc_values = []
        for desc_field in desc_fields:
            val = self.get_field_value(desc_field)
            desc_values.append(val)
        return desc_values

    def describe_with_source_field(self, desc_values):
        """
        Returns description with added/replaced wrapped source field
        """
        desc_fields = self.context['desc_fields']
        desc_format = self.context['desc_format'] 
        source_field = self.context['source_field']
        wrapped_value = self.wrap(self.get_field_value(source_field))
        if source_field in desc_fields:
            desc_values[desc_fields.index(source_field)] = wrapped_value
        elif not source_field in ["combined"]:
            desc_format += wrapped_value
        return desc_format.format(*desc_values)

    def get_field_value(self, field):
        return strip_braces(getattr(self, field)) if hasattr(self, field) else ""

    def wrap(self, string):
        wrapper = self.context['wrap_chars']
        return u'%s%s%s' % (wrapper[0], string, wrapper[1])
