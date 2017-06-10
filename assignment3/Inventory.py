import hashlib
import socket
import getpass

#pick a base port based on username   
MAX_PORT = 49152
MIN_PORT = 10000
BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % \
(MAX_PORT - MIN_PORT) + MIN_PORT + 21
 
NUM_PORTS = 2

servers = ["{host}:{port}".format(host = socket.gethostname() \
                                            , port = BASE_PORT + i) for i in range(NUM_PORTS)]

