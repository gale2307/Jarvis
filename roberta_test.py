import roberta_class
from transformers import RobertaForQuestionAnswering, RobertaTokenizer

model_name = "deepset/roberta-base-squad2"
model = RobertaForQuestionAnswering.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

while(True):
    context = input("Enter Target Filename for BERT:\n")
    if context == "exit": break
    if context[:13] != "MinecraftWiki/": context = "MinecraftWiki/" + context
    if context[-4:] != ".txt": context += ".txt"
    while(True):
        query = input("JARVIS online. What would you like to know?\n")
        if query == "exit": break
        answer, score = roberta_class.answerfromwebpage(query, context, model, tokenizer)
        print("Answer: " + answer)

