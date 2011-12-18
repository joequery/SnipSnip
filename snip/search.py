from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import *
from whoosh.qparser import QueryParser, OrGroup
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StandardAnalyzer
import inflect
from globals import *
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

		# To prevent a pluralization from causing the searches to fail,
		# store the singular version of the description string for indexing
		# and the raw sting for presentation.

		# Filename looks like so: ~/.snipsnip/python/how_to_use_lists_12342342
		fileName = os.path.join(lang_dir(lang), snippet_file_name(description))
		self.writer.add_document(
				description = unicode(self.singularize(description)),
				_stored_description = unicode(description),
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
			qp = QueryParser("description", self.ix.schema, group=OrGroup)

			# Since the index is singularized, we must search using a
			# singularized string.
			query = qp.parse(unicode("(%s) AND (lang:%s)" % (self.singularize(searchStr), lang)))
			results = searcher.search(query)
			returnThis = [ [x['description'], x['path']] for x in results]
			return returnThis

	def get_lang(self, lang):
		'''
		Get all results matching the language
		'''
		with self.ix.searcher() as searcher:
			qp = QueryParser("lang", self.ix.schema)
			query = qp.parse(unicode(lang))
			results = searcher.search(query, sortedby="description", reverse=True)
			returnThis = [ [x['description'], x['path']] for x in results]
			return returnThis
	
	def singularize(self, theStr):
		'''
		Return a singularized string. For example,
		"Rails routes variables" => "Rail route variable"
		'''
		p = inflect.engine()
		normalList = [x for x in theStr.split(' ')]
		singularList = [p.singular_noun(x) for x in normalList]

		# p.sinuglar_noun returns False if the word is already singular,
		# so just grab the word from normalList.
		returnList = [x or y for (x,y) in zip(singularList, normalList)]

		# Now join back into a string
		return " ".join(returnList)


GoogleBot = Searcher(WHOOSH_INDEX)
#result = GoogleBot.search("Hello World", "c++")
#print result[0]
