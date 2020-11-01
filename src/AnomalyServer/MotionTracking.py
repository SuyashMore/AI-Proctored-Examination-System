import cv2, time 
from datetime import datetime 

class MotionTracking:

    def __init__(self):

        self.integrity = {
            "movement" : []
        }
        self.static_back = None
        self.motion_list = [ None, None ] 
        self.motion = 0
        self.time = []
        return
    
    def run(self, frame, result):
        self.motion = 0
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
        # Converting gray scale image to GaussianBlur  
        # so that change can be find easily 
        gray = cv2.GaussianBlur(gray, (21, 21), 0) 
        if self.static_back is None:
            self.static_back = gray
            return

        # Difference between static background  
        # and current frame(which is GaussianBlur) 
        diff_frame = cv2.absdiff(self.static_back, gray) 
    
        # If change in between static background and 
        # current frame is greater than 30 it will show white color(255) 
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1] 
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
        # Finding contour of moving object 
        cnts,_ = cv2.findContours(thresh_frame.copy(),
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            self.motion = 1 
    
        # Appending status of motion 
        self.motion_list.append(self.motion)
        self.motion_list = self.motion_list[-2:] 
    
        # Appending Start time of motion 
        if self.motion_list[-1] == 1 and self.motion_list[-2] == 0: 
            self.time.append(datetime.now()) 
    
        # Appending End time of motion 
        if self.motion_list[-1] == 0 and self.motion_list[-2] == 1: 
            self.time.append(datetime.now()) 

        # Displaying the difference in currentframe to 
        # the staticframe(very first_frame) 
        cv2.imshow("Difference Frame", diff_frame) 
    
        # Displaying the black and white image in which if 
        # intensity difference greater than 30 it will appear white 
        cv2.imshow("Threshold Frame", thresh_frame)

        return
    
    def get_integrity(self):
        for i in range(0, len(self.time), 2): 
            self.integrity['movement'].append(self.time[i]) 
        return self.integrity

