import socket

s = socket.socket()
print("Created socket")

port = 8888

s.bind(('', port))
print("Binded at port: " + str(port))

s.listen(5)
print("Socket is waiting for client.")

while True:
        c, addr = s.accept()
        print("Connected from: " + str(addr))
    
        buffer = c.recv(1024)
c.close()