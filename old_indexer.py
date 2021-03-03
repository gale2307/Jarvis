#Old version of indexer; run this on the old Corpus before old_ir_tester!

import os.path
import whoosh.index as index
from whoosh.analysis import StandardAnalyzer
from whoosh.fields import *

#List of stopwords for the analyzer applied to page content
stops = frozenset(['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'yet', 'if', 'from', 'for', 'when', 'by', 'to', 'you', 'be', 'we', 'that', 'may',
                   'not', 'with', 'tbd', 'a', 'on', 'your', 'this', 'of', 'us', 'will', 'can', 'the', 'or', 'are', 'what', 'how', 'why'])

#Creates index schema; only the title is stored, and receives increased weight
schema = Schema(title=TEXT(stored=True,field_boost=3.0), content=TEXT(analyzer=StandardAnalyzer(stoplist=stops)), path=ID)

#Creates and opens index object
if not os.path.exists("oldIndex"):
    os.mkdir("oldIndex")
ix = index.create_in("oldIndex", schema)

#Creates writer
writer = ix.writer()

#Opens corpus directory and writes it all to index
for subdir, dirs, files in os.walk(r'MinecraftWiki/'):
    for filename in files:
        filepath = subdir + os.sep + filename
        print("Processing: {}\n".format(filename))
        with open(filepath, 'r', encoding="utf-8") as f:
            f_str = f.read()
            writer.add_document(title=u"{}".format(filename), path=u"{}".format(filepath), content=u"{}".format(f_str))
            f.close()

writer.commit()
