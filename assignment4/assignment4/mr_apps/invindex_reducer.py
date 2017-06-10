#!/usr/bin/env python3

import sys,pickle

postingList = {}
for line in sys.stdin:
    if not line.strip():
       continue
    
    try:
        docId, tp = line.split("\t")
        tp =  eval(tp)
        docId = int(docId)
        term =str(tp[0])
        tf = int(tp[1])
        tp = []
        if term in postingList:
            tp = postingList[term]
        tp.append((docId, tf))
        postingList[term] = tp
    except:
        pass
pickle.dump(postingList,  sys.stdout.buffer)
    
