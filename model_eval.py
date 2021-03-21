from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from f1score import get_metric_score
import bert_class
import roberta_class
import electra_class

#model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
#model_name = "deepset/bert-large-uncased-whole-word-masking-squad2"
#model = BertForQuestionAnswering.from_pretrained(model_name)
#tokenizer = BertTokenizer.from_pretrained(model_name)

model_name = "deepset/roberta-large-squad2"
#model_name = "deepset/roberta-base-squad2"
model = RobertaForQuestionAnswering.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

#model_name = "deepset/electra-base-squad2"
#model_name = "ahotrod/electra_large_discriminator_squad2_512"
#model = ElectraForQuestionAnswering.from_pretrained(model_name)
#tokenizer = ElectraTokenizer.from_pretrained(model_name)

total_score = 0.0

with open("model_eval.txt", "r") as file:
    for line in file:

        question, context, answers = line.split('|', 2)
        gold_answers = answers.split('|')

        if context[:13] != "MinecraftWiki/": context = "MinecraftWiki/" + context

        print("\nquestion: " + question)

        #ask the question to the model
        #receive predicted answer from model
        model_answer, model_score = bert_class.answerfromwebpage(question, context, model, tokenizer)

        print(gold_answers)
        score = get_metric_score(model_answer, gold_answers)
        #print question and score
        print("answer: " + model_answer)
        print("score: " + str(score))
        total_score+=score[1]

print("Total score: " + str(total_score))