#! /usr/bin/env python

import socket
import os

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 0.0.0.0 means all ips on this computer, say if we had 2 network cards
serverSocket.bind(("0.0.0.0", 12345))

# 5 is used just because they say so
serverSocket.listen(5)

while True:
    (incomingSocket, address) = serverSocket.accept()
    print str(address)

    childPid = os.fork()
    if (childPid != 0):
        #we must still be in the socket accepting process
        #if keyword 'continue' is hit, it goes back to top of loop
        continue
    #else, we must be in a client talking process

    outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    outgoingSocket.connect(("www.google.ca", 80))    

   
    done = False
    while not done:
        #fix cpu use with poll() or select()
        incomingSocket.setblocking(0)
        try:
            part = incomingSocket.recv(2048)
        except IOError, exception:
            if exception.errno == 11:
                part = None
            else:
                raise

        if (part):
            outgoingSocket.sendall(part)

        outgoingSocket.setblocking(0)
        try:
            part = outgoingSocket.recv(2048)
        except IOError, exception:
            if exception.errno == 11:
                part = None
            else:
                raise

        if (part):
            incomingSocket.sendall(part)
