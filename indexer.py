import os.path
import whoosh.index as index
from whoosh.fields import *

#Creates index schema
#Only content is stored in the index for the purpose of highlighting
schema = Schema(title=TEXT, content=TEXT(stored=True), path=ID)

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
        print("Processing: {}\n".format(filename))
        with open(filepath, 'r', encoding="utf-8") as f:
            f_str = f.read()
            writer.add_document(title=u"{}".format(filename), path=u"{}".format(filepath), content=u"{}".format(f_str))
            f.close()

writer.commit()

