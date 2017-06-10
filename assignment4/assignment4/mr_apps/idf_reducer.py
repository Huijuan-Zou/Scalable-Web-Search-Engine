#!/usr/bin/env python3

import sys,pickle, math

docIds = set()
document_count = {}
idf = {}
for line in sys.stdin:
    if not line.strip():
        continue
    term, docId = line.split("\t")
    docIds.add(docId)
    count = 0
    if term in document_count:
        count = document_count[term]
    document_count[term] = count + 1

len_ids = len(docIds)
for term in document_count.keys():
    term = str(term)
    idf[term] = math.log(len_ids) - math.log(int(document_count[term]))

pickle.dump(idf, sys.stdout.buffer)
