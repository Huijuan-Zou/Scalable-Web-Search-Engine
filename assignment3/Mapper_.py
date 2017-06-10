from tornado.web import RequestHandler
import json, subprocess, hashlib, time

mapOutput = {}

#called by Coordinate to map key-value pairs
class MapHandler(RequestHandler):
    def initialize(self, port):
        self.port = port
    def get(self):
        mapper_path = self.get_argument("mapper_path")
        input_file = self.get_argument("input_file")
        num_reducers = self.get_argument("num_reducers")
        inputFile = open(input_file)
        p = subprocess.Popen(mapper_path, stdin=inputFile, stdout=subprocess.PIPE)
        (out, _) = p.communicate()
        output = str(out.decode()).split('\n')
        lists = []
        for index in range(len(output)):
            string = output[index].strip()
            strs = string.split('\t')
            reducer_index = int(index) % int(num_reducers)
            if  len(lists) <= reducer_index:
                lists.append([])
            if not string:
                continue
            tp = lists[reducer_index]
            tmp = []
            tmp.append(strs[0])
            tmp.append(strs[1])
            tp.append(tmp)
            lists[reducer_index] =  tp
        for index in range(len(lists)):
            lista = lists[index]
            lists[index] = sorted(lista, key=lambda x: x[0])
        insertion = str(time.clock())
        length = 20
        map_task_id = hashlib.sha256(str(input_file).encode('utf-8') + insertion.encode('utf-8')).hexdigest()[:length]
        mapOutput[map_task_id] = lists
        result = {}
        result["status"] = "success"
        result["map_task_id"] = map_task_id
        self.write(json.dumps(result))
        self.finish()
            
#called by reducer to return a list of key-value pairs partition to corresponding reducer  
class RetrieveMapOutputHandler(RequestHandler):
    def initialize(self, port):
        self.port = port
    def get(self):
        map_task_id = self.get_argument("map_task_id")
        reducer_ix = self.get_argument("reducer_ix")
        result = mapOutput[map_task_id][int(reducer_ix)]
        self.write(json.dumps(result))
        self.finish()
        
