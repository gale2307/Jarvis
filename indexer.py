import os.path
import whoosh.index as index
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import *

#List of stopwords for the analyzer applied to page content
stops = frozenset(['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'yet', 'if', 'from', 'for', 'when', 'by', 'to', 'you', 'be', 'we', 'that', 'may',
                   'not', 'with', 'tbd', 'a', 'on', 'your', 'this', 'of', 'us', 'will', 'can', 'the', 'or', 'are', 'what', 'how', 'why'])

#Creates index schema; only the title is stored, and receives increased weight
schema = Schema(fullTitle=ID(stored=True), content=TEXT(analyzer=StemmingAnalyzer(stoplist=stops)), title=TEXT(analyzer=StemmingAnalyzer(stoplist=stops),field_boost=3.0))

#Creates and opens index object
if not os.path.exists("index"):
    os.mkdir("index")
ix = index.create_in("index", schema)

#Creates writer
writer = ix.writer()

#Opens corpus directory and writes it all to index
for subdir, dirs, files in os.walk(r'MinecraftWiki/'):
    for filename in files:
        filepath = subdir + os.sep + filename
        short_title = filename[30:].rstrip(".txt").replace("_", " ")
        print("Processing: {} (full title: {})\n".format(short_title, filename))
        with open(filepath, 'r', encoding="utf-8") as f:
            f_str = f.read()
            writer.add_document(fullTitle=u"{}".format(filename), content=u"{}".format(f_str), title=u"{}".format(short_title))
            f.close()

writer.commit()

