from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import bert_class

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')\

while(True):
    context = input("Enter Target Filename for BERT:\n")
    if context == "exit": break
    if context[:13] != "MinecraftWiki/": context = "MinecraftWiki/" + context
    if context[-4:] != ".txt": context += ".txt"
    while(True):
        query = input("JARVIS online. What would you like to know?\n")
        if query == "exit": break
        answer, score = bert_class.answerfromwebpage(query, context, model, tokenizer)
        print("Answer: " + answer)
