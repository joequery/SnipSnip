from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import *
from whoosh.qparser import QueryParser, OrGroup
schema = Schema(description=TEXT(stored=True), path=ID(stored=True), lang=TEXT)
from curseshelpers import *

class Searcher:
	'''
	Our search engine class! I, for one, welcome our Googly overlords.
	'''

	def __init__(self, indexdir):
		# Open the index if it exists
		try:
			ix = open_dir(indexdir)
			print "FOUND"
		except EmptyIndexError:
			ix = create_in(indexdir, schema)
		writer = ix.writer()

	def add_snippet_to_index(self, description, lang):
		fileName = file_name_from_string(description)
		writer.add_document(
				description = unicode(description),
				path = unicode(fileName),
				lang = unicode(lang)
		)
		text_editor(fileName)
		writer.commit()
	
	@staticmethod
	def search(self, searchStr, lang):
		with ix.searcher() as searcher:
			qp = QueryParser("description", ix.schema, group=OrGroup)
			query = qp.parse(unicode("(%s) AND (lang:%s)" % (searchStr, lang)))
			results = searcher.search(query)
		return results

GoogleBot = Searcher("indexdir")
