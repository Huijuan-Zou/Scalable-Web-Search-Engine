from tornado.web import RequestHandler, url
from collections import OrderedDict
import json
from tornado import gen
from tornado import httpclient
from Inventory import NUM_INDEX_PORTS,NUM_DOC_PORTS, K, INDEX_URLS, DOC_URLS

class SearchHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        query_argument = self.get_argument('q')
        def handle_response(response):
            if response.error:
                print ("Error: %s" % response.error)
            else:
                print(response.body)
        http_client = httpclient.AsyncHTTPClient()
        #fetch from index servers
        indexLists = []
        for num in range(0, NUM_INDEX_PORTS):
            url = INDEX_URLS[num] + "?q=" + str(query_argument)
            response = yield  http_client.fetch(url, handle_response) 
            body = json.loads(response.body.decode('utf-8'))
            #process data from index servers, keep only top  K pairs
            for item in body["postings"]:
                if len(indexLists) <= 0:
                    indexLists.append(item)
                else:
                    i = len(indexLists) - 1
                    while item[1] > indexLists[i][1] and i >= 0:
                        i = i - 1
                    if i < 0:
                        
                        indexLists.insert(0, item)
                    else:
                        indexLists.insert(i + 1, item)
                if len(indexLists) > K:
                    indexLists.pop()
                    
        # get results from document servers
        docList = []
        for num in range(0, len(indexLists)):
            print(int(indexLists[num][0]) % NUM_DOC_PORTS)
            print (indexLists[num][0])
            url = DOC_URLS[int(indexLists[num][0]) % NUM_DOC_PORTS] + "?id=" + str(indexLists[num][0]) + "&&q=" + str(query_argument)
            response = yield http_client.fetch(url, handle_response)
            body = json.loads(response.body.decode('utf-8'))
            for item in body["results"]:
                docList.append(item)
        result = OrderedDict()
        result["num_results"] = len(docList)
        result["results"] = docList
        self.write(json.dumps(result))
        self.finish()
