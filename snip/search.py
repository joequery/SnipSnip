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

		# pathName looks like so: python/how_to_use_lists_12342342
		# fileName is the absolute path to the pathName on the system.
		fileName = snippet_file_name(description)
		pathName = os.path.join(lang_dir(lang, False), fileName)

		self.writer.add_document(
				description = unicode(self.singularize(description).lower()),
				_stored_description = unicode(description),
				path = unicode(pathName),
				lang = unicode(lang)
		)

		fileName = os.path.join(lang_dir(lang), fileName)
		text_editor(fileName)
		self.writer.commit()
	
	def add_file_to_index(self, path, description):
		'''
		Add a snippet that already exists on the file system to the index
		'''
		self.get_writer()
		lang = path.split('/')[0]

		self.writer.add_document(
				description = unicode(self.singularize(description).lower()),
				_stored_description = unicode(description),
				path = unicode(path),
				lang = unicode(lang)
		)

		self.writer.commit()
	
	def delete(self, path):
		'''
		Delete a snippet from the index and the file system.
		path is the lang/snippetDescription path of the snippet
		'''
		
		lang = path.split('/')[0]
		snippet = path.split('/')[1]
		self.get_writer()

		# Delete based on the path, since it is unique.
		self.writer.delete_by_term('path', path)
		self.writer.commit()

		# Now that we've deleted the snippet from the index, we delete
		# it from the file system.

		# Get the full path of the snippet file.
		snipLoc = os.path.join(lang_dir(lang), snippet)

		# Now we delete it! We're done!
		os.remove(snipLoc)
	
	def rename(self, path, newDescription):
		'''
		Update a snippet based on the path. Add a new description via newDescription
		'''

		# 1. Store the contents of the snippet file in path 
		# 2. Get filename from newDescription and copy contents 
		# 3. Delete the snippet and remove from index
		# 4. Create new snippet

		# 1. Store the contents of the old snippet file 
		lang = path.split('/')[0]
		oldSnippetFileName = path.split('/')[1]
		oldSnippetLoc = os.path.join(lang_dir(lang), oldSnippetFileName)
		f = open(oldSnippetLoc, 'r')
		snippetContent = f.read()
		f.close()

		# 2. Get filename from newDescription and copy contents 
		newFileName = snippet_file_name(newDescription)
		newLoc = os.path.join(lang_dir(lang), newFileName)
		f = open(newLoc, 'w')
		f.write(snippetContent)
		f.close()

		# 3. Delete the snippet and remove from index
		self.delete(path)

		# 4. Create new snippet
		newPath = os.path.join(lang_dir(lang, False), newFileName)
		self.add_file_to_index(newPath, newDescription)


	
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
			returnThis = [ (x['description'].lower(), x['path']) for x in results]
			return returnThis

	def get_lang(self, lang):
		'''
		Get all results matching the language
		'''
		with self.ix.searcher() as searcher:
			qp = QueryParser("lang", self.ix.schema)
			query = qp.parse(unicode(lang))
			results = searcher.search(query, sortedby="description")
			returnThis = [ (x['description'].lower(), x['path']) for x in results]

			# Sort by alphabet, case insensitive
			returnThis.sort(key=lambda x:x[0].lower())
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


########################################################
# Whoosh helper functions
########################################################

def file_name_safe(theStr, joinChar='_'):
	'''
	Return a file name safe string. Extracts groups of numbers
	and letters from the string and joins with joinChar. Also
	lower cases the string.
	'''
	tmpList = re.findall(r'[a-zA-Z0-9]+', theStr)
	return joinChar.join([x.lower() for x in tmpList])


def snippet_file_name(description):
	'''
	Get a file safe name for the description with a timestamp 
	attached to avoid collisions.
	'''
	joinChar = '_'
	description = file_name_safe(description, joinChar)

	# Join with underscores and make lowercase.
	return joinChar.join([description, str( int(time.time()) )])

def lang_dir(lang, full=True):
	'''
	Get a string representing the directory of the language
	full: If full is True, get the absolute path to the file.
	'''
	if full:
		return os.path.join(SNIPPETS_DIR, lang.lower().strip())
	else:
		return lang.lower().strip()


def quick_read(fileName):
	f = open(fileName, 'r')
	items = sorted([x.strip() for x in f.readlines()], key=str.lower)
	f.close()
	return items

GoogleBot = Searcher(WHOOSH_INDEX)
#result = GoogleBot.search("Hello World", "c++")
#print result[0]
