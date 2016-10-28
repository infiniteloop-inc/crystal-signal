#!/usr/bin/python
import os
import socket
import threading
import SocketServer
from time import sleep

# - - - - - - - - - - - - - - - - 
# - - - SOCKET CLIENT CLASS - - -
# - - - - - - - - - - - - - - - -
def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        # wait for the python script to produce and send the data
        sleep(0.3)
        response = sock.recv(1048576)
        print "Content-type: text/html \n\n"
        print response
    finally:
        sock.close()

# - - - - - - - - - - - - - - - - 
# - - - - SENDING DATA  - - - - -
# - - - - - - - - - - - - - - - -
query_string=os.environ["QUERY_STRING"]
if query_string == "":
    query_string = ""

remote_addr = os.environ["REMOTE_ADDR"]

client('localhost', 7777, query_string + "&remote_addr=" + remote_addr)


