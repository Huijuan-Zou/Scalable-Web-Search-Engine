from Inventory import BASE_PORT, NUM_INDEX_PORTS
from tornado.ioloop import IOLoop
from tornado import process
from tornado.web import Application
from IndexServer import IndexHandler
from FrontEndServer import SearchHandler
from DocumentServer import documentHandler

def main():
    task_id = process.fork_processes(NUM_INDEX_PORTS + NUM_INDEX_PORTS + 1)
    if task_id == 0:
        app = Application([
        (r"/search", SearchHandler),  ])
        app.listen(BASE_PORT)
        print(BASE_PORT)
    elif task_id <= NUM_INDEX_PORTS:
        port = BASE_PORT + task_id 
        app = Application([
        (r"/index",IndexHandler, dict(port = port)),  ])
        app.listen(port)
    else:
        port = BASE_PORT + task_id
        app = Application([
        (r"/doc",documentHandler, dict(port = port)),  ])
        app.listen(port)
    IOLoop.current().start()
if __name__ == "__main__":
    main()
