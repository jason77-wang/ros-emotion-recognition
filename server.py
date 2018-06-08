import socket
import cv2
import numpy
import struct

address = ('0.0.0.0', 8002)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(True)

def sendall(sock, str):
    sock.send(str)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

conn, addr = s.accept()
while 1:
    length = recvall(conn,16)
    print "Get data length:",length
    stringData = recvall(conn, int(length))
    data = numpy.fromstring(stringData, dtype='uint8')
    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER',decimg)

    reply = struct.pack('!iiii3s', 100, 100, 300, 250, "cry")
    sendall(conn, str(len(reply)).ljust(16))
    sendall(conn, reply)
    
    if cv2.waitKey(10) == 27:
        break
    
s.close()
cv2.destroyAllWindows()
