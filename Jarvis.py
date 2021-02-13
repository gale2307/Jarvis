from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import whoosh.index as index
from whoosh.searching import Searcher
from whoosh.qparser import QueryParser
from whoosh.highlight import WholeFragmenter
import bert_class

#model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
#tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = BertForQuestionAnswering.from_pretrained('deepset/bert-large-uncased-whole-word-masking-squad2')
tokenizer = BertTokenizer.from_pretrained('deepset/bert-large-uncased-whole-word-masking-squad2')

#Opens index
ix = index.open_dir("index")

while(True):
    #Lets the user ask a query
    query = input("\nJARVIS online. What would you like to know?\n")
    if query == "exit()":
        break

    #Handles query
    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(query)

    #Searches index for query, returns best-matching page(s)
    with ix.searcher() as searcher:
        results = searcher.search(q)
        max_score = -99
        max_answer = ""
        for i in range(3):
            print(results[i]['title'])
            cur_answer, cur_score = bert_class.answerfromwebpage(query, "MinecraftWiki/" + results[i]['title'], model, tokenizer)
            print("Candidate Answer = " + cur_answer)
            print("Candidate Score = " + str(cur_score))
            if cur_score > max_score:
                max_score = cur_score
                max_answer = cur_answer
        print("Answer = " + max_answer)
