#!/usr/bin/env python
# -*- coding:utf-8 -*-
import face_recognition
import cv2
import sys,time
from sys import getsizeof
import os,shelve
import numpy as np
import rospy
from sensor_msgs.msg import Image
from track.msg import kinect
from std_msgs.msg import Bool,String
from transfer_client import transfer
from transfer_client import connectsvr

#kinect 订阅后，如果为1，则发送图片，为0停止
pub = rospy.Publisher('want_pic', Bool, queue_size=1)
#发送检测人脸结果，格式为'FaceDetect;0;' or 'FaceDetect;1;,,,;'   
#与识别到的配对最好的人脸，格式'figure;{};\n'.format(name)'
pub_num = rospy.Publisher('detect_msg',String,queue_size=1)

#pub_name = rospy.Publisher('recog_name',String,queue_size=1)


def face_detect(frame):
	rospy.loginfo('start detect!')

	small_frame=cv2.resize(frame,(0,0),fx=0.5,fy=0.5)
		# Find all the faces and face encodings in the current frame of video
	face_locations = face_recognition.face_locations(small_frame)
	face_location_ret =[]
	rospy.loginfo('start drawing box')
	# Display the results
	for (top, right, bottom, left) in face_locations:
		top*=2
		right*=2
		bottom*=2
		left*=2
		
		face_location_ret.append(str(left))
		face_location_ret.append(str(top))
		face_location_ret.append(str(right))
		face_location_ret.append(str(bottom)+';')
		
		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#		
	# Display the resulting image
	cv2.imshow('Faces', frame)
	cv2.waitKey(1)
	rospy.loginfo('Finish detection!')
	return len(face_locations),face_location_ret



def vid_callback(data):
	
	width,height = data.width,data.height
	
	np_arr = np.fromstring(data.data, np.uint8).reshape(1,-1)
	frame = np_arr.reshape(height,width,3)

        transfer(frame)


if __name__ == '__main__':

        con = 0
        sub = 0
        
	rospy.init_node('emotion_recognition', anonymous=False)
	
	rate = rospy.Rate(1)
	
	while not rospy.is_shutdown():
                if con == 0 :
                        con = connectsvr()
                elif sub == 0 :
                        rospy.Subscriber("camera/image", Image, vid_callback)
                        sub = 1
	        #set want_pic to 1 to tell other node send pic to me
                if sub == 1 :
			pub.publish(1)
		
	rate.sleep()
	
	rospy.spin()

