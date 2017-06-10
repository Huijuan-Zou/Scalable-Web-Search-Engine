from tornado.web import RequestHandler
from Indexer import docStores, processText
from Inventory import NUM_DOC_PORTS
import json

class color:
    BOLD = "<strong>"
    END = "</strong>"
   
class documentHandler(RequestHandler):
    def initialize(self, port):
        self._port = port
        
    def get(self):
        query_argument = self.get_argument('q')
        docId = self.get_argument('id')
        # get docStore from corresponding partition
        docStore = docStores[int (docId) % NUM_DOC_PORTS]
        triplet = docStore[docId]
        title = triplet[0]
        url = triplet[1]
        text = triplet[2]
        query_terms = processText(query_argument)
        
        def enBold(text, query_terms):
            for query in query_terms:
                po = text.lower().find(query)
                size = len(query)
                if po != -1:
                   text = text[:po] + color.BOLD + text[po : po + size] + color.END + text[po + size :]
            return text
        #function to get snippet
        def getSnippet(query_terms, text):
            pos = -1
            size = 0
            text = enBold(text, query_terms)  
            for query in query_terms:
                pos = text.lower().find(query)
                size = len(query)
                if pos != -1:
                    break
            snippet = ""
            if pos != -1:
                i = pos - 1
                snippet = text[pos: pos + size]
                count = 0
                while i >= 0:
                    snippet = text[i] + snippet
                    if text[i] == " ":
                        count = count + 1
                    if count >= 20:
                        break
                    i = i - 1
                if count >= 20:
                    snippet = "..." + snippet
                i = pos + size
                count = 0
                while i < len(text):
                    snippet = snippet + text[i]
                    i = i + 1
                    if text[i] == " ":
                        count = count + 1
                    if count >= 20:
                        break
            if count >= 20:
                snippet = snippet + "..."
            return snippet
        
        #get snippet
        snippet = getSnippet(query_terms, text)
        title = enBold(title, query_terms)
        tripDict = {}
        tripDict["title"] = title
        tripDict["url"] = url
        tripDict["snippet"] = snippet.replace("[", " ").replace("]", " ")\
        .replace("{", " ").replace("}", " ").replace("=", " ").replace("\n", " ")
        tripDict["doc_id"] = docId
        outList = []
        outList.append(tripDict) 
        result = {}
        result["results"] = outList
        self.write(json.dumps(result))
        self.finish()
