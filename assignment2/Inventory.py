import hashlib
import socket
import getpass

#pick a base port based on username   
MAX_PORT = 49152
MIN_PORT = 10000
BASE_PORT = int(hashlib.md5(getpass.getuser().encode()).hexdigest()[:8], 16) % \
 (MAX_PORT - MIN_PORT) + MIN_PORT

#static backend configuration
NUM_INDEX_PORTS = 3
NUM_DOC_PORTS = 3
K = 10
FILE_NAME =  "info_ret.xml"
INDEX_URLS = ["http://{host}:{port}/index".format(host = socket.gethostname(), port = BASE_PORT + i + 1) for i in range(NUM_INDEX_PORTS)]
DOC_URLS = ["http://{host}:{port}/doc".format(host = socket.gethostname(), port = BASE_PORT + NUM_INDEX_PORTS + i + 1) for i in range(NUM_INDEX_PORTS)]

        
        
        
