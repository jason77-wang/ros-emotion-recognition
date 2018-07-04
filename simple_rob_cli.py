import socket
import cv2
import numpy

address = ('127.0.0.1', 8002)
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(address)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

while True:
    rstr = recvall(sock, 64)
    print rstr


sock.close()
cv2.destroyAllWindows()
