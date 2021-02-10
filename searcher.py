import whoosh.index as index
from whoosh.searching import Searcher
from whoosh.qparser import QueryParser
from whoosh.highlight import WholeFragmenter

#Opens index
ix = index.open_dir("index")

#Lets the user ask a query
query = input("JARVIS online. What would you like to know?\n")

#Handles query
qp = QueryParser("content", schema=ix.schema)
q = qp.parse(query)

#Searches index for query, returns highlights of best-matching page
with ix.searcher() as searcher:
    results = searcher.search(q)
    #Alter maxchars, surround, and top to get more relevant highlights
    results.fragmenter.maxchars = 100
    results.fragmenter.surround = 30
    print(results[0].highlights("content", top=4))
