import socket

serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 999

serverSock.bind(('',port))
serverSock.listen(10)

while True:
    clientSock, addr = serverSock.accept()
    print("Got Connection from %s" % str(addr))
    msg = "Yes Yes Yes Thank YOu"
    clientSock.send(msg.encode('ascii'))
    
