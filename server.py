import sys
import threading
import socket
import  argparse
import signal

import os
import tqdm
count = 1
# Making Custom Thread

class myThread(threading.Thread):
    def __init__(self,serverfd):
        threading.Thread.__init__(self)
        self.serverfd = serverfd
        global count
        self.num = count
        count+=1
    def run(self):
        print("Server Has Starting")
        self.serverfd.listen()
        conn,addr = self.serverfd.accept()
        with conn:
            print("Connected by ",addr)
            while True:
                data = conn.recv(1024)
                print(data.decode())
            
            



# Handling arguments passing  ::::::::::::::::::::::
my_parser = argparse.ArgumentParser()
my_parser.add_argument('-i', action='store', required=True)
my_parser.add_argument('-n', action='store', required=True, type=int)
my_parser.add_argument('-f', action='store', required=True ,type=str)
my_parser.add_argument('-p', action='store',nargs='+',type=int, required=True)
args = my_parser.parse_args()
# End of Handling Arguments
HOST = "127.0.0.1"

portnumbers = args.p  # Extracting port numbers

numberOfServers = args.n # Extracting number of Servers
serverSockets = list()


for i in range(numberOfServers):
    serverSockets.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
    serverSockets[i].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSockets[i].bind((HOST,portnumbers[i]))
    newThread = myThread(serverSockets[i])
    newThread.start()
    newThread.join()
    
for i in range(len(portnumbers)):
    print(serverSockets[i])


