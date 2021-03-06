from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import bert_class

model = BertForQuestionAnswering.from_pretrained('deepset/bert-large-uncased-whole-word-masking-squad2')
tokenizer = BertTokenizer.from_pretrained('deepset/bert-large-uncased-whole-word-masking-squad2')

bert_class.jarvis(model, tokenizer)
