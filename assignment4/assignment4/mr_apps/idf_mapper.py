#!/usr/bin/env python3

import sys
from xml.dom import  minidom

def processText(text):
    # pre-process text -- get rid of special symbols
    text = text.replace("}", " ").replace("{"," ").replace("?"," ").replace(","," ") \
    .replace("."," ").replace("[", " ").replace("]"," ").replace("="," ").replace("'"," ").replace("\""," ") \
    .replace("("," ").replace(")"," ").replace("*"," ").replace("|"," ").replace("#"," ").replace("!"," ") \
    .replace(":"," ").replace("<"," ").replace(">"," ").replace("/"," ").replace("\t", " ")
    terms = text.lower().split(" ")
    #get rid of spaces and empty value
    newTerms = []
    for term in terms:
        newTerm = term.strip()
        if newTerm:
            newTerms.append(newTerm)
    return newTerms
        
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
for i in range(len(titles)):
    docId = docIds[i]
    text = docTexts[i]
    title = docTitles[i]
    newTerms = processText(text)
    newTitles = processText(title)
    terms = set()
    for term in newTerms:
        terms.add(term)
    for term in newTitles:
        terms.add(term)
    for term in terms:
        print('%s\t%s' % (term, docId))
