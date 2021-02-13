---
layout: default
title: Status
---

## Status Check Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/mOvRFeuM_wM" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Project Summary
Jarvis aims to be an End-to-End Question Answering System in Minecraft that answers the players questions about the game through the chatbox. When asked a question, Jarvis fetches what it thinks is the most relevant answer from Minecraft Wikipedia and returns it to the user in-game.

## Approach
Our approach involves integrating a custom information retrieval system with the NLP model BERT. Specifically, we are using the BERT-Large Uncased model pre-trained on the SQuad 1.1 dataset for Question Answering. 

Pre-setup starts with creating the corpus that JARVIS will search and retrieve answers on. To create the corpus, we first crawl on the Minecraft Wiki, saving certain text snippets from each page. The corpus is then indexed using Whoosh, an IR library, to create a schema focused on the title and content of each page, then writing the index based on that. For the index schema, more weight is placed on the page’s title to try and improve search results. No other ranking system is currently implemented otherwise. JARVIS also needs to load in some pre-trained models for its natural language processing.
	
Once this is all done, JARVIS is ready to answer questions. It takes in a typed query from the user and uses Whoosh to parse the query. This parsed query is passed to Whoosh’s searcher, which returns the top 10 results. For the sake of time, only the top 3 pages are considered. Each page is preprocessed and split into paragraphs, each paragraph tokenized before being fed into the BERT model. 
For each paragraph, BERT assigns a start-score and an end-score for each token, which is the likelihood of that token being the start or the end of the answer to the query respectively. It then returns the answer candidate for that paragraph beginning with the highest start-score token and ending with the highest end-score token. Currently, we assign each candidate a total score that is the sum of its highest start-score and highest end-score. The candidate with the highest total score is chosen as the answer. This process is similarly repeated for each webpage, and the answer with the highest total score is chosen and returned to the user.

## Evaluation

## Remaining Goals and Challenges
Currently, Jarvis still has a lot of aspects that need to be improved. Our priority will be to improve Jarvis’ accuracy, both for the IR system and the Question Answering model. For the IR, we are looking to implement common methods of improvement such as stemming, removing duplicate pages, and tf-idf. Given sufficient improvements, we are considering the possibility of expanding our corpus (such as by adding articles from Digminecraft), since much of the information in the Minecraft Wikipedia is contained within images, which Jarvis cannot use. Overall, we are hoping to get our IR system’s accuracy even with, if not close enough to, Google or Minecraft Wiki’s built-in search. For the Question Answering model, we are looking to fine-tune BERT to make it familiar with Minecraft terminology. We are also considering alternatives to BERT, which we will test and compare with BERT’s performance accordingly.

Accuracy aside, we are looking for methods to improve Jarvis’ speed. Currently, the long running time is caused by our BERT model having to go through each article paragraph by paragraph - as such, articles with numerous short paragraphs take a long time to process. Reducing the number of paragraphs by combining them or by filtering out unnecessary paragraphs are methods of improvement that we are looking to test in the near future.

Finally, we will need to integrate Jarvis with the Minecraft Malmo client. While we expect this to be trivial, unforeseen issues may appear. As such, we are planning to work on integration as soon as possible to deal with said issues.

## Resources Used
- https://github.com/google-research/bert#pre-trained-models - These pre-trained models for BERT are necessary for having NLP working with JARVIS.
- https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad - Pre-trained model that we used
- https://colab.research.google.com/drive/1uSlWtJdZmLrI3FCNIlUHFxwAJiSu2J0-#scrollTo=_xN5f1bxf6K_ - Helped us setup BERT for question answering
- https://whoosh.readthedocs.io/en/latest/index.html - Whoosh has been instrumental in creating an IR system to use with BERT, since the Anserini Retriever that came with BERTserini did not work for us.
- https://minecraft.gamepedia.com/Minecraft_Wiki - This is the site we used to get JARVIS’s corpus.