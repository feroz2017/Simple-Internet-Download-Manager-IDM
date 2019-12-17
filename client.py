import sys
import threading
import socket
import  argparse
count = 1
# Making Custom Thread

class myThread(threading.Thread):
    def __init__(self,sockfd):
        threading.Thread.__init__(self)
        self.sockfd = sockfd
        self.num = count
        count+=1
    def run(self):
        while True:
            getData = self.sockfd.recv(1024)
            print("From Server ",self.count,getData)



# Handling arguments passing  ::::::::::::::::::::::
my_parser = argparse.ArgumentParser()
my_parser.add_argument('-i', action='store', required=True)
my_parser.add_argument('-r', action='store_true', required=False)
my_parser.add_argument('-o', action='store', required=True)
my_parser.add_argument('-a', action='store', required=True)
my_parser.add_argument('-p', action='store',nargs='+',type=int, required=True)
args = my_parser.parse_args()
# End of Handling Arguments
HOST = args.a # Extracting Server IP Address

portnumbers = args.p  # Extracting port numbers
clientSockets = list()


for i in range(len(portnumbers)):
    clientSockets.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
    clientSockets[i].bind((HOST,portnumbers[i]))
    newThread = myThread(clientSockets[i])
    newThread.start
    
for i in range(len(portnumbers)):
    print(clientSockets[i])


