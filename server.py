import socket

s = socket.socket()
print("Created socket")

port = 8888

s.bind(('', port))
print("Binded at port: " + str(port))

while True:
        c, addr = s.accept()
        print("Connected from: " + str(addr))
    
        buffer = c.recv(1024)
c.close()