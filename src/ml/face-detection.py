import cv2
import sys

# CONFIG
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
fair_count, total_count, none_buffer, more_buffer = 0, 0, 0, 0


# WEBCAM
video_capture = cv2.VideoCapture(0)


# LOOP
while True:

    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    total_count += 1
    fair_count += 1
    count_of_faces = len(faces)

    if(count_of_faces == 1):
        none_buffer = 0
        more_buffer = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    else:
        if count_of_faces == 0:
            none_buffer += 1
        else:
            more_buffer += 1

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
    if (more_buffer == 50):
        fair_count -= 50
        more_buffer = 0
        # GIVE WARNING FOR MORE THAN ONE PERSON ON SCREEN
        cv2.putText(frame, "More than one person detected!!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))


    elif(none_buffer == 100):
        fair_count -= 100
        none_buffer = 0
        # GIVE WARNING FOR NO ONE ON SCREEN
        cv2.putText(frame, "No one detected!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))




    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Show Integrity Score
integrity_score = fair_count/ total_count
print(integrity_score)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
