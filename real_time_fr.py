import face_recognition
from cv2 import *
import numpy as np
#import mail_send as mail
import sendmail as mail
import time

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
kirk_image = face_recognition.load_image_file("./known/kirk.jpg")
kirk_face_encoding = face_recognition.face_encodings(kirk_image)[0]

# Load a second sample picture and learn how to recognize it.
chet_image = face_recognition.load_image_file("./known/chet.jpg")
chet_face_encoding = face_recognition.face_encodings(chet_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    kirk_face_encoding,
    chet_face_encoding
]
#Test Dataset
known_face_names = [
    "Kirk Fay",
    "Chet Timsina"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
#Create a boolean flag to reduce email spam
#We will also start a timer in order to realert someone if the person is
#Still there in 5 minutes
status = False
firstTime = time.time()
secondTime = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        imwrite("intruder_img.jpg",frame)
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                secondTime = time.time()
                if status == True and ((secondTime - firstTime) > 300):
                    firstTime = time.time()
                    secondTime = time.time()
                    mail.send()
                if status == False:
                    status = True
                    secondTime = time.time()
                    mail.send()
            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
