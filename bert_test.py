import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def answer_question(question, answer_text):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.
    input_ids = tokenizer.encode(question, answer_text)

    # Report how long the input sequence is.
    print('Query has {:,} tokens.\n'.format(len(input_ids)))

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    # ======== Evaluate ========
    # Run our example question through the model.
    start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids])) # The segment IDs to differentiate question from answer_text

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    start_max = torch.max(start_scores)
    end_max = torch.max(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):
        
        # If it's a subword token, then recombine it with the previous token.
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        
        # Otherwise, add a space then the token.
        else:
            answer += ' ' + tokens[i]

    return answer, start_max.item(), end_max.item()

def answerfromwebpage(question, path):

    max_score = -99 #set to 0?
    max_answer = ""

    with open(path, "r", encoding='utf-8') as f:
        for context in f:
            cur_answer, cur_start, cur_end = answer_question(question, context)
            print("Context: " + context)
            print('Answer: "' + cur_answer + '"')
            print('Start: ' + str(cur_start))
            print('End: ' + str(cur_end))
            if max_score < (cur_start + cur_end):
                max_answer = cur_answer
                max_score = cur_start + cur_end

    return max_answer

q0 = "What is the crafting recipe for a wooden sword"
q1 = "How many articles are in this wiki"
q2 = "What is minecraft"
q3 = "How much does minecraft java edition cost"
q4 = "How much Minecraft: Java Edition cost"
q5 = "When was minecraft pocket edition released"

answer = answerfromwebpage(q0, "MinecraftWikiTest/https_minecraft_gamepedia_com_Sword.txt")
print(answer)
