#pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f
#pip install opencv-contrib-python
#pip install face-recognition

import face_recognition
import cv2
import numpy as np

video_capture = cv2.VideoCapture(0)

# LOAD 
# USER IMAGE FROM CLOUD BUCKET => user_image
# USER ID => user_id

# WARNING BUFFER LIMIT (CAN BE PROVIDED BY ADMIN)
not_matching_limit = 50
more_person_limit = 30
no_person_limit = 50

user_image = face_recognition.load_image_file("dataset/1.jpg") # to be loaded from bucket
user_encoding = face_recognition.face_encodings(user_image)[0] 
student_id = 1  # student id from database
user_id = str(student_id)
user_encoding_list = [user_encoding]

# RED FLAG DETAILS
total_frames = 0
no_person_frames = 0
more_person_frames = 0
fair_frames = 0
not_matching_frames = 0

# COUNT OF WARNINGS
not_matching_warning = 0
more_person_warning = 0
no_person_warning = 0


# WARNING BUFFERS
not_matching_buffer = 0
more_person_buffer = 0
no_person_buffer = 0


def reset_buffer():
    not_matching_buffer = 0
    more_person_buffer = 0
    no_person_buffer = 0
    return

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    # total frame count
    total_frames += 1
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
      
    number_of_faces = len(face_encodings)

    if (number_of_faces > 1): 
        more_person_frames += 1
        not_matching_buffer = 0
        no_person_buffer = 0
        more_person_buffer += 1

    elif (number_of_faces == 0): 
        no_person_frames += 1
        not_matching_buffer = 0
        more_person_buffer = 0
        no_person_buffer += 1

    elif (number_of_faces == 1):
        face_distance = face_recognition.face_distance(user_encoding_list, face_encodings[0]) [0]
        if face_distance < 0.6:
            reset_buffer()
            fair_frames += 1

        else: 
            not_matching_frames += 1
            not_matching_buffer += 1
            no_person_buffer = 0
            more_person_buffer = 0

    # GIVE WARNING FOR NO ONE ON SCREEN
    if no_person_buffer >= no_person_limit:
        if (no_person_buffer % no_person_limit == 0): 
            no_person_warning += 1
        cv2.putText(frame, "No one detected!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    
    # GIVE WARNING FOR MORE ON SCREEN
    elif more_person_buffer >= more_person_limit:
        if (more_person_buffer % more_person_limit == 0): more_person_warning += 1
        cv2.putText(frame, "More than on person detected!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    
    # GIVE WARNING FOR NOT A MATCH 
    elif not_matching_buffer >= not_matching_limit:
        if (not_matching_buffer % no_matching_limit == 0): not_matching_warning += 1
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
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print("TOTAL FRAMES: ", total_frames)
print("MATCHED FRAMES: ", fair_frames)
print("NO PERSON FRAMES: ", no_person_frames)
print("MORE THAN ONE PERSON FRAMES: ", more_person_frames)
print("NOT MATCHED FRAMES: ", not_matching_frames)
print("No PERSON WARNINGS: ", no_person_warning)
print("MORE THAN ONE PERSON WARNINGS: ", more_person_warning)
print("NOT MATCHED WARNINGS: ", not_matching_warning)

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
