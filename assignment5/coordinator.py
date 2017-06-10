from argparse import ArgumentParser
from tornado.ioloop import IOLoop
from tornado import gen, httpclient
from inventory import NUM_WORKERS, servers
from urllib.parse import urlencode
import os, importlib,pickle

global files, cur_model, app, compute_gradient, gradients

@gen.coroutine
def calc_partial_gradient():
    global files, cur_model, compute_gradient, gradients
    http = httpclient.AsyncHTTPClient()
    postdata = (compute_gradient, cur_model)
    body = pickle.dumps(postdata)
    num_files = len(files)
    futures = {}
    for index in range(num_files):
        for i in range(NUM_WORKERS):
            if index % NUM_WORKERS == i:
                url = "http://%s/compute_gradient?input_file=%s" \
                %(servers[i], files[index])
                request = httpclient.HTTPRequest(url, method='POST', headers=None, body=body )
                print(request)
                futures[index] = http.fetch(request)
    responses = yield futures
    for index in range(len(responses)):
        response = responses[index]
        responseBody = pickle.loads(response.body)
        gradients[index] = responseBody
    
def main():
    parser = ArgumentParser()
    parser.add_argument("--app", dest = "apps",required=True)
    parser.add_argument("--job_path", dest = "job_path", required=True)
    parser.add_argument("--iterations", dest = "iterations", type = int, required=True)
    args = parser.parse_args()
    global files, cur_model, app, iterations, compute_gradient, gradients
    app = args.apps
    print(app)
    job_path = args.job_path
    iterations = args.iterations
    
    files = []
    for f in os.listdir(job_path):
        if f.endswith('.in'):
            files.append(job_path + "/" + f)

    word2vec = importlib.import_module(app)
    init_model = getattr(word2vec, 'init_model')
    cur_model = init_model(files)
    print(cur_model)
    compute_gradient = getattr(word2vec, 'compute_gradient')
    update_model = getattr(word2vec, 'update_model')
    
    num_files = len(files)
    gradients = {}
    
    while iterations >= 0:
        IOLoop.current().run_sync(calc_partial_gradient)
        for index in range(num_files):
            update_model(cur_model, gradients[index])
        iterations -= 1
    outFile = str(job_path) + "/0.out"
    with open(outFile, 'wb') as f:
        f.write(pickle.dumps(cur_model))
    
if __name__ == "__main__":
    main()