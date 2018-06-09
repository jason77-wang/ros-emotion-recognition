
# coding: utf-8

# In[ ]:


import socket
import numpy as np
import random,time
import struct
import scipy.io as sio
import os, sys, cv2

#%matplotlib inline

CLASSES = ('__background__','face','mask')
    
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

if __name__ == '__main__':

    TCP_IP = ''
    TCP_PORT = 5001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  
    s.bind((TCP_IP, TCP_PORT))
    s.listen(5)
    print "Listening on port",TCP_PORT,"......"

    while True:
        try:
            conn, addr = s.accept()

            print "connected by:",addr

            while True:
                length = recvall(conn,16)
                if not length: 
                    print "No connection"
                    break
                stringData = recvall(conn, int(length))
                if not stringData: 
                    print "No data received"
                    break
                data = np.fromstring(stringData, dtype='uint8')
                decimg=cv2.imdecode(data,1)
                decimg = decimg[:, :, (2, 1, 0)]
                               
                #add random box instead model
                detectresult = []
                img_h,img_w,c = decimg.shape
                rnd_class = CLASSES[random.randint(1,2)]
                rnd_x1 = random.randint(0,img_w/2)
                rnd_y1 = random.randint(0,img_h/2)
                rnd_x2 = rnd_x1+random.randint(0,img_w/2)
                rnd_y2 = rnd_y1+random.randint(0,img_h/2)
                detectresult.append((rnd_class,(rnd_x1,rnd_y1,rnd_x2,rnd_y2)))
                x1 = 0
                y1 = 0
                x2 = 0
                y2 = 0
                for class_name,position in detectresult:
                    x1 = int(position[0])
                    y1 = int(position[1])
                    x2 = int(position[2])
                    y2 = int(position[3])
                    structstr = struct.pack('!iiii%ds' % len(class_name),x1,y1,x2,y2,class_name)
                    conn.send(str(len(structstr)).ljust(16))
                    conn.send(structstr)
            
                structstr = struct.pack('!iiii%ds' % len('end'),x1,y1,x2,y2,'end')
                conn.send(str(len(structstr)).ljust(16))
                conn.send(structstr)
                cv2.waitKey(1)
        except:
            print 'Disconnect with:',addr
            continue

    s.close()

