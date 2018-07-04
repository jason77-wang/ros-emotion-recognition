
# coding: utf-8

# In[ ]:


import socket
import numpy as np
import random,time
import struct
#import scipy.io as sio
import os, sys, cv2

#%matplotlib inline

CLASSES = ('__background__','face','mask')

speech_connected = "speech:机器人连接成功"
speech_wounded = "speech:前方发现伤员"
speech_aidbox = "speech:请使用急救箱中的工具进行救治"
speech_warn = "speech:大家注意,发现可疑人员"


eye_close = "eye:0"
eye_half = "eye:1"
eye_open = "eye:2"

drawer_close = "drawer:0"
drawer_open = "drawer:1"

head_up = "head:0"
head_down = "head:1"

arm_down = "arm:0"
arm_up = "arm:1"

startpoint = "startpoint:0,0"
destination_forward = "destination:10,10"
destination_back = "destination:0,0"

pack_len = 64

def fake_delay():
    time.sleep(5)
    return

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


def connected_greeting(sock):
    sendall(sock, speech_connected.ljust(pack_len))
    fake_delay()
    sendall(sock, eye_close.ljust(pack_len))
    fake_delay()
    sendall(sock, eye_half.ljust(pack_len))
    fake_delay()
    sendall(sock, eye_open.ljust(pack_len))
    fake_delay()
    sendall(sock, eye_half.ljust(pack_len))
    fake_delay()
    sendall(sock, eye_close.ljust(pack_len))
    fake_delay()


def found_wounded(sock):
    sendall(sock, speech_wounded.ljust(pack_len))
    fake_delay()
    sendall(sock, speech_aidbox.ljust(pack_len))
    fake_delay()
    sendall(sock, drawer_close.ljust(pack_len))
    fake_delay()
    sendall(sock, drawer_open.ljust(pack_len))
    fake_delay()
    sendall(sock, drawer_close.ljust(pack_len))
    fake_delay()


def found_badguy(sock):
    sendall(sock, speech_warn.ljust(pack_len))
    fake_delay()
    sendall(sock, head_up.ljust(pack_len))
    fake_delay()
    sendall(sock, head_down.ljust(pack_len))
    fake_delay()
    sendall(sock, head_up.ljust(pack_len))
    fake_delay()
    sendall(sock, arm_down.ljust(pack_len))
    fake_delay()
    sendall(sock, arm_up.ljust(pack_len))
    fake_delay()
    sendall(sock, arm_down.ljust(pack_len))
    fake_delay()


def move_test(sock):
    sendall(sock, startpoint.ljust(pack_len))
    fake_delay()
    sendall(sock, destination_forward.ljust(pack_len))
    fake_delay()
    sendall(sock, destination_back.ljust(pack_len))
    fake_delay()

if __name__ == '__main__':

    TCP_IP = ''
    TCP_PORT = 8002
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
                connected_greeting(conn)
                found_wounded(conn)
                found_badguy(conn)
                move_test(conn)
                time.sleep(20)
                print "I am alive"

        except:
            print 'Disconnect with:',addr
            break

    s.close()

