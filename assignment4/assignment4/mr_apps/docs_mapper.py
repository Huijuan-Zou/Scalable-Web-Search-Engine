#!/usr/bin/env python3

import sys
from xml.dom import  minidom

doc = minidom.parse(sys.stdin)
texts = doc.getElementsByTagName("text")
docTexts = []
for text in texts:
    text = text.firstChild.nodeValue
    text = text.replace("[", " ").replace("]", " ")\
        .replace("{", " ").replace("}", " ").replace("=", " ") \
        .replace("\n", " ").replace("\t", " ")
    docTexts.append(text)
titles = doc.getElementsByTagName("title")
docTitles = []
for title in titles:
    title = title.firstChild.nodeValue
    title = title.replace("[", " ").replace("]", " ")\
        .replace("{", " ").replace("}", " ").replace("=", " ") \
        .replace("\n", " ").replace("\t", " ")
    docTitles.append(title)
numDocs = len(docTitles)
ids = doc.getElementsByTagName("id")
docIds = []
for mId in ids:
    if (mId.parentNode.nodeName == "page"):
        docIds.append(mId.firstChild.nodeValue)
for i in range(len(docIds)):
    docId = docIds[i]
    value = str((docTitles[i],docTexts[i]))
    print('%s\t%s' % (docId, value))

    
