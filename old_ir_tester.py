#Run old_indexer first!

import sys

import whoosh.index as index
import whoosh.qparser as qparser
from whoosh.searching import Searcher

correct = 0
queries = 0

#Opens index
ix = index.open_dir("oldIndex")

#Opens test file
with open(sys.argv[1], 'r') as f:
    while True:
        #Reads next query/url pair
        line = f.readline()
        if not line:
            break
        
        #Loads query and expeced answer
        query = line.split(';')[0]
        expected = line.split(';')[1].rstrip('\n')
        retrieved = []
        found = False
        queries += 1

        #Handles query
        qp = qparser.QueryParser("content", schema=ix.schema)
        q = qp.parse(query)

        #Searches index for query, checks top 3 URLs for expected URL
        with ix.searcher() as searcher:
            results = searcher.search(q)
            #Correctness metric: Is our expected URL in the top 3?
            for i in range(3):
                retrieved.append(results[i]['title'])
                if expected == retrieved[i]:
                    correct += 1
                    found = True
            print("Query {}:".format(queries), query)
            print("URL:", expected)
            if found:
                print("PASSED")
            else:
                print("FAILED")
            #Uncomment to print top 3 URLs from IR
            #print("{}\n{}\n{}\n".format(retrieved[0], retrieved[1], retrieved[2]))


print("{} / {} queries matched.".format(correct, queries))
print("Accuracy: ", float(correct/queries))
