from whoosh.index import create_in, open_dir, EmptyIndexError
from whoosh.fields import *
from whoosh.qparser import QueryParser, OrGroup
schema = Schema(description=TEXT(stored=True), path=ID(stored=True), lang=TEXT)

# Open the index if it exists
try:
	ix = open_dir("indexdir")
	print "FOUND"
except EmptyIndexError:
	ix = create_in("indexdir", schema)


writer = ix.writer()
writer.add_document(
description=u"Route segment key constraints",
path=u"/rails/route_segment_key_constraints.rb",
lang=u"ruby"
)
writer.add_document(
description=u"Route variables",
path=u"/rails/route_segment_keys.rb",
lang=unicode("ruby")
)
writer.commit()
with ix.searcher() as searcher:
	query = QueryParser("description", ix.schema, group=OrGroup).parse(unicode("(Rails route variables) AND (lang:ruby)"))
	results = searcher.search(query)
	for x in results:
		print x
