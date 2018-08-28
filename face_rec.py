import face_recognition
import cv2
import os

# Initialize some variables
known_face_encodings = []
known_face_names = []
face_locations = []
face_encodings = []
face_names = []


def get_names_from_image(team):
    global known_face_encodings
    global known_face_names
    print("Initializing images for "+str(team)+"...")
    #load all available images
    for n, image_file in enumerate(os.scandir('img/'+team+"/")):
        image = face_recognition.load_image_file(image_file.path)
        known_face_encodings.append(face_recognition.face_encodings(image)[0])
        known_face_names.append(os.path.splitext(image_file)[0].split('/')[2])


def get_faces(frame, face_in_scene):

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
        name = "Person"

        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if (name != 'Person'):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 8
            right *= 8
            bottom *= 8
            left *= 8

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            face_in_scene.append(name)

    return frame
