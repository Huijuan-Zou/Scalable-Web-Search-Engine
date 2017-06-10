from Inventory import NUM_DOC_PORTS, NUM_INDEX_PORTS, FILE_NAME
from collections import Counter
from xml.dom import  minidom

def processText(text):
    # pre-process text -- get rid of special symbols
    text = text.replace("}", " ").replace("{"," ").replace("?"," ").replace(","," ") \
    .replace("."," ").replace("[", " ").replace("]"," ").replace("="," ").replace("'"," ").replace("\""," ") \
    .replace("("," ").replace(")"," ").replace("*"," ").replace("|"," ").replace("#"," ").replace("!"," ") \
    .replace(":"," ").replace("<"," ").replace(">"," ").replace("/"," ")
    terms = text.lower().split(" ")
    #get rid of spaces and empty value
    newTerms = []
    for term in terms:
        newTerm = term.strip()
        if newTerm:
            newTerms.append(newTerm)
    return newTerms
    
#adding term frequency to postinglist
def getTermFrequency(postingLists, docId, text, title):
    #process document text and title
    newTerms = processText(text)
    newTitles = processText(title)
              
    #term frequency in current doc text
    termFrequencyDict = Counter(newTerms)
    # term frequency in current doc title
    titleFrequencyDict = Counter(newTitles)
    
    #calculating final term frequency
    num_shard = int (docId) % NUM_INDEX_PORTS
    postingList = {}
    if num_shard in postingLists:
        postingList = postingLists[num_shard]
    for term in termFrequencyDict:
        tp = {}
        if term in postingList:
            tp = postingList[term]
        # final term frequency is a sum of term Frequency in doc text and doc title
        tp[docId] = termFrequencyDict[term] * 1 + titleFrequencyDict[term] * 10
        postingList[term] = tp  
    postingLists[num_shard] = postingList
    
def main(fileName):
    docStores = {}
    postingLists = {}
    doc = minidom.parse(fileName)
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
        getTermFrequency(postingLists, docIds[i], docTexts[i], docTitles[i])
    urls = []
    for title in docTitles:
        titleSplit = title.split(" ")
        title = ""
        i = 0
        while i < len(titleSplit) - 1:
            title += titleSplit[i] + "_"
            i += 1
        if i >= 0:
            title += titleSplit[i]
        if isinstance(title, str):
            title = str(title.encode('utf8'))
        else:
            title = str(unicode(title).encode('utf8'))
        url = "https://en.wikipedia.org/wiki/" + title
        urls.append(url)  
        
    #map title, url and text to document id
    for i in range(len(urls)):
        docId = docIds[i]
        #partition to shards
        num_shard = int(docId) % NUM_DOC_PORTS
        docStore = {}
        if num_shard in docStores:
            docStore = docStores[num_shard]
        docStore[docId] = (docTitles[i], urls[i], docTexts[i])
        docStores[num_shard] = docStore
    return [postingLists, docStores, numDocs]

triplet = main(FILE_NAME)
postingLists = triplet[0]
docStores = triplet[1]
numDocs = triplet[2] 



