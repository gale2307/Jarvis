import torch
import whoosh.index as index
import whoosh.scoring as scoring
from whoosh.searching import Searcher
from whoosh.qparser import QueryParser
from whoosh.qparser import OrGroup
from whoosh.qparser import MultifieldParser
from whoosh.highlight import WholeFragmenter

def answer_question(question, input_ids, model, tokenizer):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.
    '''
    # ======== Tokenize ========
    # Apply the tokenizer to the input text, treating them as a text-pair.
    #input_ids = tokenizer.encode(question, answer_text)

    # Report how long the input sequence is.
    #print('Query has {:,} tokens.\n'.format(len(input_ids)))

    #Prevents inputs longer than 512
    if len(input_ids) > 512:
        return "Number of tokens exceed 512", -10, -10

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    #Filters out short contexts
    if len(input_ids) - sep_index < 10:
        return "Context is too short", -10, -10

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
    # The problem is somewhere around here, to do with token_type_ids
    outputs = model(torch.tensor([input_ids]))#, token_type_ids=torch.tensor([segment_ids])) # The segment IDs to differentiate question from answer_text

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    start_max = torch.max(start_scores)
    end_max = torch.max(end_scores)
    
    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    if tokens[answer_start][0] == 'Ġ':
        answer = tokens[answer_start][1:]
    else:
        answer = tokens[answer_start]

    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start + 1, answer_end + 1):
        #answer += ' ' + tokens[i]
        
        # If it's a subword token, then recombine it with the previous token.
       if tokens[i][0:2] == '##':
            answer += tokens[i][2:] 
       # Otherwise, add a space then the token.
       else:
           answer += ' ' + tokens[i]

    if "[CLS]" in answer: return answer, -10, -10
    return answer, start_max.item(), end_max.item()

def answerfromwebpage(question, path, model, tokenizer):

    max_score = -99 #set to 0?
    max_answer = ""

    with open(path, "r", encoding='utf-8') as f:
        context_string = ""
        for context in f:
            if len(tokenizer.encode(question, context)) > 512: continue

            input_tokens = tokenizer.encode(question, context_string + context)
            context_string += context
            #print("CONTEXT: " + context)
            #print("CONTEXT STRING: " + context_string)

            if len(input_tokens) > 0:
                #input_tokens = tokenizer.encode(question, context_string)
                #print("Context: " + context_string)
                cur_answer, cur_start, cur_end = answer_question(question, input_tokens, model, tokenizer)
                #print("Context: " + context)
                #print('Answer: "' + cur_answer + '"')
                #print('Start: ' + str(cur_start))
                #print('End: ' + str(cur_end))
                if max_score < (cur_start + cur_end):
                    max_answer = cur_answer
                    max_score = cur_start + cur_end


                context_string = ""

            #context_string += context

        if not(context_string == ""):
            input_tokens = tokenizer.encode(question, context_string)
            #print("Context: " + context_string)
            cur_answer, cur_start, cur_end = answer_question(question, input_tokens, model, tokenizer)
            if max_score < (cur_start + cur_end):
                max_answer = cur_answer
                max_score = cur_start + cur_end

    return max_answer, max_score

def get_answers(model, tokenizer, query, ix):
    #Handles query
    og = OrGroup.factory(0.9)
    qp = MultifieldParser(["title", "content"], schema=ix.schema, group=og)
    q = qp.parse(query)

    #Searches index for query, returns best-matching page(s)
    with ix.searcher(weighting=scoring.BM25F(B=0.75, content_B=1.0, K1=1.5)) as searcher:
        results = searcher.search(q)
        max_score = -99
        max_answer = ""
        for i in range(3):
            print(results[i]['fullTitle'])
            cur_answer, cur_score = answerfromwebpage(query, "MinecraftWiki/" + results[i]['fullTitle'], model, tokenizer)
            if cur_score > max_score:
                max_score = cur_score
                max_answer = cur_answer
    return max_answer

def jarvis(model, tokenizer):

    #Opens index
    ix = index.open_dir("index")

    while(True):
        #Lets the user ask a query
        query = input("JARVIS online. What would you like to know?\n")
        if query == "exit()":
            break

        max_answer = get_answers(model, tokenizer, query, ix)
        print("Answer = " + max_answer)
