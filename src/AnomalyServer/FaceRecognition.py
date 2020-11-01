import face_recognition
import cv2
import numpy as np

class FaceRecognition:

    def __init__(self, user_image, user_id, no_person_limit = 50, more_person_limit = 30, not_matching_limit = 50):

        self.integrity = {
            "no_person":{
                "frames": 0,
                "warnings": 0,
                "buffer": 0,
                "limit": no_person_limit
            },

            "more_person":{
                "frames": 0,
                "warnings": 0,
                "buffer": 0,
                "limit": more_person_limit
            },

            "no_match":{
                "frames": 0,
                "warnings": 0,
                "buffer": 0,
                "limit": not_matching_limit
            },
            "total_frames": 0,
            "fair_frames": 0
        }
        user_image = face_recognition.load_image_file(user_image) # to be loaded from bucket
        user_encoding = face_recognition.face_encodings(user_image)[0] 
        self.user_encoding = [user_encoding]
        self.user_id = user_id
        return
    
    def raise_warning(self, np=False, mp = False, nm=  False):
        if np == True:
            self.integrity['no_person']['warnings'] += 1
        elif mp == True:
            self.integrity['more_person']['warnings'] += 1
        elif nm == True:
            self.integrity['no_match']['warnings'] += 1
        
        return
        

    def raise_frame(self, np=False, mp = False, nm=  False):
        if np == True:
            self.integrity['no_person']['frames'] += 1
            self.integrity['no_person']['buffer'] += 1
            self.integrity['more_person']['buffer'] = 0
            self.integrity['no_match']['buffer'] = 0
        elif mp == True:
            self.integrity['more_person']['frames'] += 1
            self.integrity['more_person']['buffer'] += 1
            self.integrity['no_person']['buffer'] = 0
            self.integrity['no_match']['buffer'] = 0
        elif nm == True:
            self.integrity['no_match']['frames'] += 1
            self.integrity['no_match']['buffer'] += 1
            self.integrity['no_person']['buffer'] = 0
            self.integrity['more_person']['buffer'] = 0
        return

    def reset_buffer(self):
        for k in ('no_person', 'more_person', 'no_match'):
            self.integrity[k]['buffer'] = 0
        return

    def run(self, frame, result):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        # total frame count
        self.integrity['total_frames'] += 1

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        number_of_faces = len(face_encodings)

        if (number_of_faces > 1): 
            self.raise_frame(mp=True)

        elif (number_of_faces == 0): 
            self.raise_frame(np=True)

        elif (number_of_faces == 1):
            face_distance = face_recognition.face_distance(self.user_encoding, face_encodings[0]) [0]
            if face_distance < 0.6:
                self.reset_buffer()
                self.integrity['fair_frames'] += 1

            else: 
                self.raise_frame(nm=True)

        # GIVE WARNING FOR NO ONE ON SCREEN
        if self.integrity['no_person']['buffer'] >= self.integrity['no_person']['limit']:
            if (self.integrity['no_person']['buffer'] % self.integrity['no_person']['limit'] == 0): 
                self.raise_warning(np=True)
            cv2.putText(frame, "No one detected!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        
        # GIVE WARNING FOR MORE ON SCREEN
        elif self.integrity['more_person']['buffer'] >= self.integrity['more_person']['limit']:
            if (self.integrity['more_person']['buffer'] % self.integrity['more_person']['limit'] == 0): 
                self.raise_warning(mp=True)
            cv2.putText(frame, "More than on person detected!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        
        # GIVE WARNING FOR NOT A MATCH 
        elif self.integrity['no_match']['buffer'] >= self.integrity['no_match']['limit']:
            if (self.integrity['no_match']['buffer'] % self.integrity['no_match']['limit'] == 0): 
                self.raise_warning(nm=True)
            cv2.putText(frame, "Verified User Not found!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

        # Display the results
        for top, right, bottom, left in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display the resulting image
        result.write(frame)
        return
    
    def get_integrity(self):
        return self.integrity