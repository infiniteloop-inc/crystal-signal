#!/usr/bin/python
import os
import socket
import threading
import SocketServer

# - - - - - - - - - - - - - - - - 
# - - - SOCKET CLIENT CLASS - - -
# - - - - - - - - - - - - - - - -
def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        printHTML = False;
        if not "json=1" in message.lower():
            printHTML = True;
        print "Content-type: text/html \n\n"
        if printHTML:
            print
            with open('ctrl_UpperHalf.html') as f:
                  print f.read()
        print response
        if printHTML:
            print
            with open('ctrl_LowerHalf.html') as f:
                  print f.read()
    finally:
        sock.close()

# - - - - - - - - - - - - - - - - 
# - - - - SENDING DATA  - - - - -
# - - - - - - - - - - - - - - - -
query_string=os.environ["QUERY_STRING"]
if query_string == "":
    query_string = ""

remote_addr = os.environ["REMOTE_ADDR"]
#remote_host = os.environ["REMOTE_HOST"]

client('localhost', 7777, query_string + "&remote_addr=" + remote_addr)


