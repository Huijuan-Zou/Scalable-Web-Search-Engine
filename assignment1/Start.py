from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
import hashlib
import getpass
import socket
from tornado import gen
from tornado import httpclient

def getPortNumber():
   MAX_PORT = 49152
   MIN_PORT = 10000
   BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % (MAX_PORT - MIN_PORT) + MIN_PORT
   print(BASE_PORT)
   return BASE_PORT

PORTS = {}
URL = {}
PORTS[1] = getPortNumber()
PORTS[2] = PORTS[1] + 1
PORTS[3] = PORTS[1] + 2
URL[1] = "http://" + socket.gethostname() + ":" + str(PORTS[1])
URL[2] = "http://" + socket.gethostname() + ":"  + str(PORTS[2])
URL[3]= "http://" + socket.gethostname() + ":"  + str(PORTS[3])
cnt = 0

class MainHandler1(RequestHandler):
    def get(self):
        self.write(URL[1])

class MainHandler2(RequestHandler):
     def get(self):
        self.write(URL[2])

class MainHandler3(RequestHandler):
     def get(self):
        self.write(URL[3])

class LoadBalancer(RequestHandler):
     @gen.coroutine
     def get(self):
        def handle_response(response):
           if response.error:
              print ("Error: %s" % response.error)
           else:
              print(response.body)

        http_client = httpclient.AsyncHTTPClient()
        global cnt
        cnt = (cnt + 1) % 3
        url = URL[1]
        if (cnt == 1):
           url = URL[2]
        elif (cnt == 2):
           url = URL[3]
        response =  yield  http_client.fetch(url, handle_response)
        self.write(response.body)
        self.finish()

if __name__ == "__main__": 
   app1 = Application([
        (r"/", MainHandler1),    ])
   app2  = Application([
        (r"/", MainHandler2),   ])
   app3  = Application([
        (r"/", MainHandler3),    ])
   app1.listen(PORTS[1])
   app2.listen(PORTS[2])
   app3.listen(PORTS[3])
   app4 = Application([
        (r"/", LoadBalancer),    ])
   app4.listen(PORTS[1] - 1)      
   print("Please connect http://linserv2.cims.nyu.edu/" + str(PORTS[1] - 1))
   IOLoop.current().start()
