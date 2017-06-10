from argparse import ArgumentParser
from Inventory import NUM_PORTS, servers
from tornado.ioloop import IOLoop
from tornado import gen, httpclient
import os, json

global mapper_path
global reducer_path
global job_path
global num_reducers
global files 
global num_files
global map_task_ids 

@gen.coroutine
def runMapper():
    http = httpclient.AsyncHTTPClient()
    global map_task_ids, mapper_path, reducer_path, job_path, files, num_reducers
    futures = {}
    
    for index in range(num_files):
        for i in range(NUM_PORTS):
            if index % NUM_PORTS == i:
                url = "http://%s/map?mapper_path=%s&input_file=%s/%s&num_reducers=%s" \
                %(servers[i], mapper_path, job_path, files[index], num_reducers)
                print("Fetching", url)
                futures[index] = http.fetch(url)
    responses = yield futures
    
    for index in range(len(responses)):
        response = responses[index]
        responseBody = json.loads(response.body.decode())
        map_task_id = responseBody["map_task_id"]
        map_task_ids[index] = map_task_id

def getString():
    res = ""
    for index in range(len(map_task_ids)):
        res = res + map_task_ids[index] + ","
    res = res[:len(res) - 1]
    return res

@gen.coroutine
def runReducer():
    http = httpclient.AsyncHTTPClient()
    map_task_ids_str = getString()
    futures =[]
    for index in range(num_reducers):
        for i in range(NUM_PORTS):
            if index % NUM_PORTS == i:
                url = "http://%s/reduce?map_task_ids=%s&reducer_path=%s&job_path=%s&reducer_ix=%s" \
                % (servers[i], map_task_ids_str,reducer_path, job_path, index)
                print("Fetching", url)
                futures.append(http.fetch(url))
    yield futures

    
def main():
    parser = ArgumentParser(description = "Starting the Coordinator...")
    parser.add_argument("--mapper_path", dest = "mapper_path")
    parser.add_argument("--reducer_path", dest = "reducer_path")
    parser.add_argument("--job_path", dest = "job_path")
    parser.add_argument("--num_reducers", dest = "num_path")
    
    args = parser.parse_args()
    global mapper_path, reducer_path, job_path, num_files, num_reducers, files, map_task_ids
    mapper_path = args.mapper_path
    reducer_path = args.reducer_path
    job_path = args.job_path
    num_reducers = int(args.num_path)
    files = [f for f in os.listdir(job_path) if f.endswith('.in')]
    num_files = len(files) 

    map_task_ids = {}
    IOLoop.current().run_sync(runMapper)
    IOLoop.current().run_sync(runReducer)
    
if __name__ == "__main__":
    main()
    
