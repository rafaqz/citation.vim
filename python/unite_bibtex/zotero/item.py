#-*- coding:utf-8 -*-

class zoteroItem(object):

	"""Represents a single zotero item."""

	def __init__(self, init=None):

		"""
		Constructor.

		Keyword arguments:
		init			--	A `dict` with item information, or an `int` with the
							item id	. (default=None)
		"""

		if isinstance(init, dict):
			if u"item_id" in item:
				self.id = item[u"item_id"]
			else:
				self.id = ""
			if u"abstract" in item:
				self.abstract = item[u"abstract"]
			else:
				self.abstract = ""
			if u"publicationTitle" in item:
				self.publication = item[u"publicationTitle"]
			else:
				self.publication = ""
			if u"title" in item:
				self.title = item[u"title"]
			else:
				self.title = ""
			if u"author" in item:
				self.authors = item[u"author"]
			else:
				self.authors = []
			if u"author" in item:
				self.authors = item[u"notes"]
			else:
				self.authors = []
			if u"date" in item:
				self.date = item[u"date"]
			else:
				self.date = ""
			if u"issue" in item:
				self.issue = item[u"issue"]
			else:
				self.issue = ""
			if u"url" in item:
				self.url = item[u"url"]
			else:
				self.url = ""
			if u"pages" in item:
				self.pages = item[u"pages"]
			else:
				self.pages = ""
			if u"pages" in item:
				self.pages = item[u"pages"]
			else:
				self.pages = ""
			if u"ISBN" in item:
				self.isbn = item[u"ISBN"]
			else:
				self.isbn = ""
			if u"DOI" in item:
				self.doi = item[u"DOI"]
			else:
				self.doi = ""
			if u"language" in item:
				self.language = item[u"language"]
			else:
				self.language = ""
			if u"publisher" in item:
				self.publisher = item[u"publisher"]
			else:
				self.publisher = ""
			if u"volume" in item:
				self.volume = item[u"volume"]
			else:
				self.volume = ""
			if u"fulltext" in item:
				self.fulltext = item[u"fulltext"]
			else:
				self.fulltext = ""
			if u"collections" in item:
				self.collections = item[u"collections"]
			else:
				self.collections = []
			if u"tags" in item:
				self.tags = item[u"tags"]
			else:
				self.tags = []
			if u"key" in item:
				self.key = item[u"key"]
			else:
				self.key = ""
		else:
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
			self.fulltext = ""
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
			return u"Unkown author"
		if len(self.authors) > 5:
			return u"%s et al." % self.authors[0]
		if len(self.authors) > 2:
			return u", ".join(self.authors[:-1]) + u", & " + self.authors[-1]
		if len(self.authors) == 2:
			return self.authors[0] + u" & " + self.authors[1]
		return self.authors[0]

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
