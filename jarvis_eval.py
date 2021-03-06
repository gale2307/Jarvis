import whoosh.index as index
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from f1score import get_metric_score
import bert_class

model = BertForQuestionAnswering.from_pretrained('deepset/bert-large-uncased-whole-word-masking-squad2')
tokenizer = BertTokenizer.from_pretrained('deepset/bert-large-uncased-whole-word-masking-squad2')

gold_answers = []
total_score = 0.0

ix = index.open_dir("index")

with open("eval.txt", "r") as file:
    for line in file: #add while loop

        question, answers = line.split('|', 1)
        gold_answers = answers.split('|')

        print("question: " + question)

        #ask the question to the model
        #receive predicted answer from model
        model_answer = bert_class.get_answers(model, tokenizer, question, ix)

        print(gold_answers)
        score = get_metric_score(model_answer, gold_answers)
        #print question and score
        print("answer: " + model_answer)
        print("score: " + str(score))
        total_score+=score[1]

print("Total score: " + str(total_score))