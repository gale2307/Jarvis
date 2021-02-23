import whoosh.index as index
import whoosh.scoring as scoring
import whoosh.qparser as qparser
from whoosh.searching import Searcher
from whoosh.highlight import WholeFragmenter

#Opens index
ix = index.open_dir("index")

while (True):
    #Lets the user ask a query
    query = input("JARVIS online. What would you like to know?\n")

    #Handles query
    og = qparser.OrGroup.factory(0.9)
    qp = qparser.MultifieldParser(["title", "content"], schema=ix.schema, group=og)
    q = qp.parse(query)

    #Searches index for query, returns best-matching page(s)
    with ix.searcher(weighting=scoring.BM25F(B=0.75, content_B=1.0, K1=1.5)) as searcher:
        results = searcher.search(q)
        for i in range(10):
            print(results[i]['fullTitle'])
        #Print highlights of best-matched page; alter maxchars, surround, and top to get more relevant highlights
        #results.fragmenter.maxchars = 100
        #results.fragmenter.surround = 30
        #print(results[0].highlights("content", top=4))
