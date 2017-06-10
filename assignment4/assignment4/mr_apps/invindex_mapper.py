#!/usr/bin/env python3

import sys
from xml.dom import  minidom
from collections import Counter

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

def getTermFrequency(docId, text, title):
    newTerms = processText(text)
    newTitles = processText(title)
    termFrequencyDict = Counter(newTerms)
    titleFrequencyDict = Counter(newTitles)
    terms_tf = {}
    lista = []
    for term in termFrequencyDict:
        term_frequency = termFrequencyDict[term] * 1 
        terms_tf[term] = term_frequency
    for term in titleFrequencyDict:
        term_frequency = 0
        if term in terms_tf:
            term_frequency =  terms_tf[term]
        term_frequency += titleFrequencyDict[term] * 10
        terms_tf[term] = term_frequency
    for term in terms_tf:
        #sys.stderr.write(value)
        lista.append((docId, (term, terms_tf[term])))
    return lista 

doc = minidom.parse(sys.stdin)
texts = doc.getElementsByTagName("text")
docTexts = []
for text in texts:
    docTexts.append(text.firstChild.nodeValue)
titles = doc.getElementsByTagName("title")
docTitles = []
for title in titles:
    docTitles.append(title.firstChild.nodeValue)
numDocs = len(docTitles)
ids = doc.getElementsByTagName("id")
docIds = []
for mId in ids:
    if (mId.parentNode.nodeName == "page"):
        docIds.append(mId.firstChild.nodeValue)
for i in range(len(titles)):
    lista = getTermFrequency(docIds[i], docTexts[i], docTitles[i]) 
    for tuple0 in lista:
        docId = tuple0[0]
        tup = tuple0[1]
        term = tup[0]
        tf = tup[1]
        value = str((term, tf))
        print('%s\t%s' % (docId, value))
