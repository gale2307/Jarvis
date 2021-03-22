from transformers import RobertaForQuestionAnswering, RobertaTokenizer
import jarvis_class

#model_name = "deepset/roberta-large-squad2"
model_name = "deepset/roberta-base-squad2"
model = RobertaForQuestionAnswering.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)


def runJarvisWithModel(query):
    return jarvis_class.jarvis(model, tokenizer, query)
