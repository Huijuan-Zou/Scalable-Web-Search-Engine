from tornado.web import RequestHandler
from Indexer import processText, postingLists, numDocs
from collections import Counter
from Inventory import NUM_INDEX_PORTS, K
import math, logging
import json

log = logging.getLogger(__name__)

class IndexHandler(RequestHandler):
    def initialize(self, port):
        self.port = port
        
    def get(self):
        query_argument = self.get_argument('q')
        terms = processText(query_argument)
        query_term_dict = Counter(terms)
        #function to get tf_idf value for term j in doc i
        def get_TF_IDF_value(termFrequency, numDoc_of_termI):
            return termFrequency * (math.log(numDocs) - math.log(numDoc_of_termI))
        #function to get a score dictionary for each document
        def getScore(query_term_dict):
            scores = {}
            for query_term in query_term_dict:
                query_term_frequency = query_term_dict[query_term]
                # get postinglist from corresponding partition
                postingList = postingLists[int(self.port) % NUM_INDEX_PORTS]
                if query_term in postingList:
                    docDict = postingList[query_term]
                    numDoc_of_termI = len(docDict)
                    for docId in docDict:
                        termFrequency = docDict[docId]
                        tf_idf = get_TF_IDF_value(termFrequency,numDoc_of_termI)
                        curSum = query_term_frequency * tf_idf
                        if docId in scores:
                            curSum = curSum + scores[docId]
                        scores[docId] = curSum
            return scores
        #function to return k document ids with top k highest scores
        def getTopK(scoreDict):
            top_k_scores = []
            for docId in scoreDict:
                if len(top_k_scores) == 0:
                    top_k_scores.append([docId, scoreDict[docId]]) 
                else:
                    i = len(top_k_scores) - 1
                    while scoreDict[docId] > top_k_scores[i][1] and i >= 0:
                        i =  i - 1
                    if i < 0:
                        top_k_scores.insert(0, [docId,scoreDict[docId]])
                    else:
                        top_k_scores.insert(i + 1, [docId,scoreDict[docId]])
                if len(top_k_scores) > K:
                    top_k_scores.pop()
            return top_k_scores
        #compute scores
        scoreDict = getScore(query_term_dict)
        # compute top k documents with top k scores
        top_k_scores = getTopK(scoreDict)
        result = {}
        result["postings"] = top_k_scores
        self.write(json.dumps(result))
        self.finish()
