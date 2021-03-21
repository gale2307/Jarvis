import electra_class
from transformers import ElectraForQuestionAnswering, ElectraTokenizer

model_name = "ahotrod/electra_large_discriminator_squad2_512"
model = ElectraForQuestionAnswering.from_pretrained(model_name)
tokenizer = ElectraTokenizer.from_pretrained(model_name)

while(True):
    context = input("Enter Target Filename for BERT:\n")
    if context == "exit": break
    if context[:13] != "MinecraftWiki/": context = "MinecraftWiki/" + context
    if context[-4:] != ".txt": context += ".txt"
    while(True):
        query = input("JARVIS online. What would you like to know?\n")
        if query == "exit": break
        answer, score = electra_class.answerfromwebpage(query, context, model, tokenizer)
        print("Answer: " + answer)

