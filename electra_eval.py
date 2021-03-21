import whoosh.index as index
from transformers import ElectraForQuestionAnswering, ElectraTokenizer
import time
from f1score import get_metric_score
import electra_class

#model_name = "deepset/electra-base-squad2"
model_name = "ahotrod/electra_large_discriminator_squad2_512"
model = ElectraForQuestionAnswering.from_pretrained(model_name)
tokenizer = ElectraTokenizer.from_pretrained(model_name)

gold_answers = []
total_score = 0.0

ix = index.open_dir("index")

start_time = time.perf_counter()
with open("eval.txt", "r") as file:
    for line in file: #add while loop

        question, answers = line.split('|', 1)
        if answers[-1:]=='\n': 
            answers = answers[:-1]
        gold_answers = answers.split('|')

        print("\nquestion: " + question)

        #ask the question to the model
        #receive predicted answer from model
        model_answer = electra_class.get_answers(model, tokenizer, question, ix)

        print(gold_answers)
        score = get_metric_score(model_answer, gold_answers)
        #print question and score
        print("answer: " + model_answer)
        print("score: " + str(score))
        total_score+=score[1]

end_time = time.perf_counter()

print(f"Ran in {end_time - start_time:0.4f} seconds")
print("Total score: " + str(total_score))