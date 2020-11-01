import face_recognition
import cv2
import numpy as np, pandas
import os, sys, dlib, imutils, time
from datetime import datetime

from FaceRecognition import FaceRecognition
from LandmarkDetection import LandmarkDetection
from UpperBodyDetection import UpperBodyDetection
from MotionTracking import MotionTracking
        
# To be loaded/streamed
video = cv2.VideoCapture(0)
# user_id = int(input("Enter USER ID "))
# user_image = input("ENTER IMAGE PATH ")
user_image = 'dataset/1.jpg'
user_id = 1

# We need to set resolutions. 
# so, convert them from float to integer. 
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
size = (frame_width, frame_height) 
result = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)      


fr = FaceRecognition(user_image, user_id)
ld = LandmarkDetection()
ud = UpperBodyDetection()
mt = MotionTracking()

while True: 
    ret, frame = video.read() 
  
    if ret == True:  

        fr.run(frame, result)
        ld.run(frame, result)
        ud.run(frame, result)
        mt.run(frame, result)
        cv2.imshow('Frame', frame) 

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # Break the loop 
    else: 
        break

video.release() 
result.release() 
# Closes all the frames 
cv2.destroyAllWindows()


integrity_score = {}
integrity_score.update(fr.get_integrity())
integrity_score.update(ld.get_integrity())
integrity_score.update(ud.get_integrity())
integrity_score.update(mt.get_integrity())

for k in integrity_score.keys():
    print(k, integrity_score[k])