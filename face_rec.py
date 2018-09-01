# il file gestisce il riconoscimento dei visi

import face_recognition
import cv2
import os

# Inizializzo variabili
known_face_encodings = []
known_face_names = []
face_locations = []
face_encodings = []
face_names = []

# salvo i nomi da associare ad ogni viso attraverso il nome del file ed il relativo face encoding
def get_names_from_image(team):
    global known_face_encodings
    global known_face_names
    print("Initializing images for "+str(team)+"...")
    #load all available images
    for n, image_file in enumerate(os.scandir('img/'+team+"/")):
        image = face_recognition.load_image_file(image_file.path)
        known_face_encodings.append(face_recognition.face_encodings(image)[0])
        known_face_names.append(os.path.splitext(image_file)[0].split('/')[2])

# la funzione cerca le facce nella scena
def get_faces(frame, face_in_scene):

    # faccio il resize del frame del video ad 1/8 della sua grandezza per ottenere una maggiore velocità di analisi
    small_frame = cv2.resize(frame, (0, 0), fx=0.125, fy=0.125)

    # converto l'immagine da bgr ad rgb
    rgb_small_frame = small_frame[:, :, ::-1]

    # trovo tutte le facce ed i face encodings nel frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # vedo se il viso trovato è tra quelli conosciuti
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
        name = "Person"

        # se è stata trovata una corrispondenza nei known_face_encodings, usa la prima
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)


    # mostro i risultati
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if (name != 'Person'):
            # ingrandisco le dimensioni delle facce di 8 volte...
            top *= 8
            right *= 8
            bottom *= 8
            left *= 8

            # ...e disegno un bounding box intorno alla faccia
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # disegno un label col nome del giocatore sotto il bounding box
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            face_in_scene.append(name)

    return frame
