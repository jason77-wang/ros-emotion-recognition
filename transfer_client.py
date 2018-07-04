# -*- coding: utf-8 -*
#!/usr/bin/env python
import socket
import cv2
import numpy as np
import random,time
import struct,math

#=============================I am split line=============================#
class Timer(object):
    """A simple timer."""
    def __init__(self):
        self.total_time = 0.
        self.calls = 0
        self.start_time = 0.
        self.diff = 0.
        self.average_time = 0.

    def tic(self):
        # using time.time instead of time.clock because time time.clock
        # does not normalize for multithreading
        self.start_time = time.time()

    def toc(self, average=True):
        self.diff = time.time() - self.start_time
        self.total_time += self.diff
        self.calls += 1
        self.average_time = self.total_time / self.calls
        if average:
            return self.average_time
        else:
            return self.diff
#=============================I am split line=============================#
def drawaim(frame, classname,x1,y1,x2,y2,color = (0,255,0)):
	#draw aim rectangle like Person of Interest
	color = (random.randint(128,255),random.randint(128,255),random.randint(128,255))
	red = (0,0,255)
	if classname == 'mask':color = red
	width = abs(x2 - x1)
	height = abs(y2 - y1)
	thickness = 2 
	step = 6
	#draw corner 
	cv2.line(frame,(x1,y1),(x1 + width/step,y1),color,thickness)
	cv2.line(frame,(x1,y1),(x1,y1 + height/step),color,thickness)
	cv2.line(frame,(x2 - width/step,y1),(x2,y1),color,thickness)	
	cv2.line(frame,(x2,y1),(x2,y1 + height/step),color,thickness)
	cv2.line(frame,(x1,y2 - height/step),(x1,y2),color,thickness)
	cv2.line(frame,(x1,y2),(x1 + width/step,y2),color,thickness)	
	cv2.line(frame,(x2 - width/step,y2),(x2,y2),color,thickness)	
	cv2.line(frame,(x2,y2 - height/step),(x2,y2),color,thickness)
	cv2.line(frame,(x2,y2 - height/step),(x2,y2),color,thickness)	
	#draw middle line
	cv2.line(frame,(x1 + width/2,y1),(x1 + width/2,y1 + height/8),color,thickness)	
	cv2.line(frame,(x1 + width/2,y2 - height/8),(x1 + width/2,y2),color,thickness)	
	cv2.line(frame,(x1,y1 + height/2),(x1 + width/8,y1 + height/2),color,thickness)	
	cv2.line(frame,(x2 - width/8,y1 + height/2),(x2,y1 + height/2),color,thickness)	
	thickness = 1
	for j in range(0,10,2):
		#draw dash line
		cv2.line(frame,(x1 + width/step + j*width*2/30,y1),(x1 + width/step + (j+1)*width*2/30 ,y1),color,thickness)
		cv2.line(frame,(x1 + width/step + j*width*2/30,y2),(x1 + width/step + (j+1)*width*2/30 ,y2),color,thickness)
		cv2.line(frame,(x1,y1 + height/step + j*height*2/30),(x1 ,y1 + height/step + (j+1)*height*2/30),color,thickness)
		cv2.line(frame,(x2,y1 + height/step + j*height*2/30),(x2 ,y1 + height/step + (j+1)*height*2/30),color,thickness)
	#Draw text box
	#cv2.rectangle(frame,(x1,y1 - 20),(x2,y1 - 3),(64,64,64),-1)
	color = (64,64,64)
	if classname == 'mask': color = red
	cv2.rectangle(frame,(x1,y1 - 20),(x2,y1 - 3),color,-1)
	cv2.rectangle(frame,(x1,y1 - 20),(x2,y1 - 3),(200,200,200),1)
	#Draw classname
	cv2.putText(frame, classname, (x1 + 3,y1 - 7), 0, 0.4, (255,255,255),1)
	#print 'Class name:',classname,'x1:',x1,'y1:',y1,'x2:',x2,'y2:',y2
	
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
def drawstat(n): #draw some statistics image
	h,w,channel = frame.shape
	#print h,w
	center = (w/8,h*9/10)
	r1 = h/10
	r2 = h/16
	#n = 0
	cv2.circle(frame,center,r1,(255,128,0),-1,0)
	cv2.circle(frame,center,r2,(96,32,0),-1,0)
	for n in range(0,n):
		p1x = int(center[0] + r1 * math.cos( n * math.pi/6))
		p1y = int(center[1] + r1 * math.sin( n * math.pi/6))
		p2x = int(center[0] + r1 * math.cos( (n + 1) * math.pi/6))
		p2y = int(center[1] + r1 * math.sin( (n + 1) * math.pi/6))
		p4x = int(center[0] + r2 * math.cos( n * math.pi/6))
		p4y = int(center[1] + r2 * math.sin( n * math.pi/6))
		p3x = int(center[0] + r2 * math.cos( (n + 1) * math.pi/6))
		p3y = int(center[1] + r2 * math.sin( (n + 1) * math.pi/6))
		pts2 = np.array([[p1x,p1y],[p2x,p2y],[p3x,p3y],[p4x,p4y]], np.int32)	
		cv2.fillConvexPoly(frame,pts2,(0,255,255),8)
#=============================I am split line=============================#

#TCP_IP = '127.0.0.1'
TCP_IP = '172.16.247.244'
#TCP_PORT = 5001
TCP_PORT = 8002

sock = socket.socket()

def connectsvr():
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #enable heartbeat
	#sock.settimeout(10)
	try:
		sock.connect((TCP_IP, TCP_PORT))
		print 'Connected to :',TCP_IP,TCP_PORT
                return 1
	except:
		print 'Can not connect to',TCP_IP,TCP_PORT
                return 0
		#print 'Retrying...'
		#sock.connect((TCP_IP, TCP_PORT))	
#=============================I am split line=============================#

#if __name__ == '__main__':
def transfer(frame):

	encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),75]
	result, imgencode = cv2.imencode('.jpg', frame, encode_param)
	data = np.array(imgencode)
	stringData = data.tostring()	
#	print "Sending data length...",
	sock.send( str(len(stringData)).ljust(16));
#	print "Done"
#	print "Sending stringData...",
	sock.send( stringData );
#	print "Done,bytes: ",len(stringData)
	lastresult = []
	classlist = []

	while True: #receive one frame detect list
		length = recvall(sock,16) #get struct length first
		print "Get data length:",length
		structstr = recvall(sock,int(length))
		print "Get data structstr:",structstr
		x1,y1,x2,y2,class_name = struct.unpack('!iiii%ds' % (int(length)-16),structstr)		
		print 'Class name:',class_name,'x1:',x1,'y1:',y1,'x2:',x2,'y2:',y2
		if class_name == 'end':
			break
		else:
			if class_name == 'no mask person':
				continue
			else:
				#drawaim(x1,y1,x2,y2,class_name)
				item = [class_name,x1,y1,x2,y2]
				lastresult.append(item)
				classlist.append(class_name)

	# probably need to pass frame as parameter?
	for class_name,x1,y1,x2,y2 in lastresult:
		drawaim(frame, class_name,x1,y1,x2,y2)
	cv2.imshow('CLIENT',frame)
	cv2.waitKey(1)
