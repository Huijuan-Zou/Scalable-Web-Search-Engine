from tornado.web import RequestHandler
from tornado import gen, httpclient
import json, subprocess
from Inventory import servers

class ReduceHandler(RequestHandler):
    def initialize(self, port):
        self.port = port
        
    @gen.coroutine   
    def get(self):
        http = httpclient.AsyncHTTPClient()
        futures = []

        tasks = self.get_argument("map_task_ids")
        map_task_ids = tasks.split(",")
        reducer_path = self.get_argument("reducer_path")
        reducer_ix = self.get_argument("reducer_ix") 
        outFile_path = self.get_argument("job_path")
        num_mappers = len(map_task_ids)
        
        for i in range(num_mappers):
            server = servers[int(i) % len(servers)]
            url = "http://%s/retrieve_map_output?reducer_ix=%s&map_task_id=%s" \
            % (server, reducer_ix, map_task_ids[i])
            print("Fetching", url)
            futures.append(http.fetch(url))
        responses = yield futures
        
        kv_pairs = []
        for r in responses:
            print(json.loads(r.body.decode()))
            kv_pairs.extend(json.loads(r.body.decode()))
        kv_pairs.sort(key=lambda x: x[0])
        kv_string = "\n".join([pair[0] + "\t" + pair[1] for pair in kv_pairs])
        outFile = open(str(outFile_path) + "/" + str(reducer_ix) + ".out", 'w')
        p = subprocess.Popen(reducer_path, stdin=subprocess.PIPE, stdout=outFile)
        p.communicate(kv_string.encode())
        outFile.close()
        result = {}
        result["status"] = "success"
        self.write(json.dumps(result))
        self.finish()