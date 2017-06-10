from Inventory import NUM_PORTS, BASE_PORT
from tornado.ioloop import IOLoop
from tornado.web import Application
from Mapper_ import MapHandler, RetrieveMapOutputHandler
from Reducer_ import ReduceHandler
from tornado import process

def main():
    task_id =  process.fork_processes(NUM_PORTS)
    port = BASE_PORT + task_id
    print (port)
    app = Application([(r"/map", MapHandler, dict(port = port)),
                       (r"/retrieve_map_output", RetrieveMapOutputHandler, dict(port = port)),
                       (r"/reduce", ReduceHandler, dict(port = port))  ])
    app.listen(port)
    IOLoop.current().start()
    
if __name__ == "__main__":
    main()
