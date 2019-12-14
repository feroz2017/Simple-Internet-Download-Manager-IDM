import socket

clientSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

port = 999

clientSock.connect(('localhost',port))
msg  = clientSock.recv(1024)

clientSock.close()

print(msg.decode('ascii'))