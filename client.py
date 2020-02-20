import sys
import threading
import socket
import  argparse
import signal
import os
from tqdm import tqdm
import shutil

#os.mkdir("/root/IDM/A")
count = 1
# Making Custom Thread
os.makedirs("/root/IDM/A", exist_ok=True)

videoParts = []

lock = threading.Lock()

class myThread(threading.Thread):
    def __init__(self,id,sockfd):
        threading.Thread.__init__(self)
        self.sockfd = sockfd
        self.id=id
        global count
        self.num = count
        count+=1
        self.daemon = True;
        self.daemon = False
        partnum = self.id
        self.filename = os.path.join('A', ('part%04d.mp4' % partnum))
    def run(self):
        part = open(self.filename,"+ab")
        print("Thead Fuck You")
        file_size = int(self.sockfd.recv(2025).decode())
        print(file_size)
        progress = tqdm(total=int(file_size))
        while True:
            if file_size < 0:
                break
            getData = self.sockfd.recv(2024)
            part.write(getData)
            file_size = file_size- 2024
            #print(file_size)
            progress.update(len(getData))
        part.close()
        with lock:
            with open(self.filename,"rb") as part:
                videoParts.append(part.read())
        self.sockfd.close()



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

output_location = args.o




clientSockets = list()
threads = []

for i in range(len(portnumbers)):
    clientSockets.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
    clientSockets[i].connect((HOST,portnumbers[i]))
    newThread = myThread(i,clientSockets[i])
    newThread.start()
    threads.append(newThread)
    
for i in range(len(portnumbers)):
    print(clientSockets[i])


while True:
    inn = input(":")
    if(inn == "resume"):
        print("Resume")
    elif inn == "pause":
        print("Pause")
    elif inn == "exit":
        break



for t in threads:
    t.join()

#with open("kakaka.mp4","wb") as f:
#   for i in videoParts:
#        print(i)
#        f.write(i)




readsize = 1024

def join(fromdir, tofile):
    print(fromdir)
    print(tofile)
    output = open(tofile, 'wb')
    parts  = os.listdir(fromdir)
    print(os.listdir)
    parts.sort(  )
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(readsize)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close(  )
    output.close()


join("A",output_location)
shutil.rmtree("/root/IDM/A")