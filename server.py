import sys
import threading
import socket
import  argparse
import signal
import time

import os
import tqdm
count = 1


kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(3 * megabytes)
# Making Custom Thread

class myThread(threading.Thread):
    def __init__(self,id,serverfd,data):
        threading.Thread.__init__(self)
        self.serverfd = serverfd
        global count
        self.num = count
        count+=1
        self.id = id
        self.data = data
    def run(self):
        print("Server Has Starting")
        self.serverfd.listen(1)
        conn,addr = self.serverfd.accept()
        conn.sendall((str(len(self.data))).encode())
        time.sleep(3)
        with conn:
            print("Connected by ",addr)
            conn.sendall(self.data)
            while True:
                data = conn.recv(1024)
            

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


# video spliting

chunks = []

filename = "Test.mp4"
filesize = os.path.getsize(filename)
print(numberOfServers)
chunksize = int(filesize/(numberOfServers))
inputs = open(filename, 'rb')         
partnum = 0          
while 1:
    chunk = inputs.read(chunksize)
    if not chunk: break 
    chunks.append(chunk)
    partnum  = partnum+1                                              
inputs.close( )



threads = []
print(len(chunks))
for i in range(numberOfServers):
    serverSockets.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
    serverSockets[i].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSockets[i].bind((HOST,portnumbers[i]))
    newThread = myThread(i,serverSockets[i],chunks[i])
    newThread.start()
    threads.append(newThread)
    
for i in range(len(portnumbers)):
    print(serverSockets[i])


for t in threads:
    t.join()