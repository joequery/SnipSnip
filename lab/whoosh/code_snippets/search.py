from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser, OrGroup
schema = Schema(description=TEXT(stored=True), path=ID(stored=True))
ix = create_in("indexdir", schema)
writer = ix.writer()
writer.add_document(
		description=u"Route segment key constraints",
		path=u"/rails/route_segment_key_constraints.rb"
		)
writer.add_document(
		description=u"Route variables",
		path=u"/rails/route_segment_keys.rb"
		)
writer.commit()
with ix.searcher() as searcher:
	    query = QueryParser("description", ix.schema, group=OrGroup).parse(unicode("Rails route variables"))
	    results = searcher.search(query)
	    print results

