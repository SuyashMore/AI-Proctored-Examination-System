import cv2
import imutils
from datetime import datetime

class UpperBodyDetection:

    def __init__(self):
        self.haar_upper_body_cascade = cv2.CascadeClassifier("AnomalyServer\weights\haarcascade_upperbody.xml")
        self.integrity = {
            'extra-people-found': []
        }
    
    def run(self, frame, result):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert video to grayscale
        upper_body = self.haar_upper_body_cascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (50, 100), # Min size for valid detection, changes according to video size or body size in the video.
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        if len(upper_body) >= 1:
            self.integrity['extra-people-found'].append(datetime.now())

        # Draw a rectangle around the upper bodies
        for (x, y, w, h) in upper_body:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1) # creates green color rectangle with a thickness size of 1
            cv2.putText(frame, "Upper Body Detected", (x + 5, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # creates green color text with text size of 0.5 & thickness size of 2
        
        result.write(frame)
        return
    
    def get_integrity(self):
        return self.integrity
    

    