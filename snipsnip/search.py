from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import *
from whoosh.qparser import QueryParser, OrGroup
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StandardAnalyzer
ana = StandardAnalyzer(
    expression=re.compile(r"[\w\-+]+(\.?[\w\-]+)*", re.UNICODE),
    stoplist=None,
    minsize=0
)

schema = Schema(description=TEXT(stored=True), path=ID(stored=True), lang=TEXT(analyzer=ana, multitoken_query="phrase"))
from curseshelpers import *

class Searcher:
	'''
	Our search engine class! I, for one, welcome our Googly overlords.
	'''

	def __init__(self, indexdir):
		# Open the index if it exists
		try:
			self.ix = open_dir(indexdir)
		except EmptyIndexError:
			self.ix = create_in(indexdir, schema)
		self.indexdir = indexdir

	def get_writer(self):
		self.writer = self.ix.writer()

	def add_snippet_to_index(self, description, lang):
		''' Add a new code snippet to the index.
		description: description of the index
		lang: the language/framework.
		
		s.add_snippet_to_index("Append to list", "Python")
		'''

		self.get_writer()
		fileName = file_name_from_string(description)
		self.writer.add_document(
				description = unicode(description),
				path = unicode(fileName),
				lang = unicode(lang)
		)
		text_editor(fileName)
		self.writer.commit()
	
	def search(self, searchStr, lang):
		''' Search for a code snippet based off a search string (searchStr)
		and the language

		s.search("How to append to a list", "Python")
		'''
		with self.ix.searcher() as searcher:
			#qp = QueryParser("description", self.ix.schema, group=OrGroup)
			qp = QueryParser("description", self.ix.schema)
			query = qp.parse(unicode("(%s) AND (lang:%s)" % (searchStr, lang)))
			results = searcher.search(query)
		return results

	def get_lang(self, lang):
		'''
		Get all results matching the language
		'''
		with self.ix.searcher() as searcher:
			qp = QueryParser("lang", self.ix.schema)
			query = qp.parse(unicode(lang))
			print query
			results = searcher.search(query)
			returnThis = [x['description'] for x in results]
			return returnThis
	
	def open_snippet(self, description):
		'''
		Open the snippet from the description in the text editor
		'''
		fileName = file_name_from_string(description)
		text_editor(fileName)

GoogleBot = Searcher("indexdir")
