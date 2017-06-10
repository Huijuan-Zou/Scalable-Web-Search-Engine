#!/usr/bin/env python3

import sys,pickle

documentStore = {}
for line in sys.stdin:
    if not line.strip():
        continue
    docId, tp = line.split("\t")
    #docId = decodeBinary(docId)
    #tp = decodeBinary(tp)  
    #title, text = tp.split("=")
    tp = eval(tp)
    docId = int(docId)
    title = str(tp[0])
    text = str(tp[1])
    documentStore[docId] = (title, text)
    
pickle.dump(documentStore,  sys.stdout.buffer)
