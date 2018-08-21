import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import datetime
from oologic.event import Event
from get_color import detect_color
from get_scene_change import is_new_scene,count_distance
from face_rec import get_faces, get_names_from_image
from oologic.create_test_match import createMatch
from get_options import get_opt

temp_opt = get_opt()

option = {
    'model': 'cfg/tiny-yolo-voc-2c.cfg',
    'load': int(temp_opt[2]),
    'threshold': float(temp_opt[1]),
    'gpu': 1.0
}

match = createMatch()
frame_rate_originale = int(temp_opt[3])
tfnet = TFNet(option)
last_tag_time = 0
capture = cv2.VideoCapture(str(temp_opt[0]))
num_frame_scena = 0

current_frame_scena = 0
num_frame = 0
temp_num_frame = 1
count = 0
count_event = 0
event_on = False
tabellone_on = False
old_ratio = [0, 0, 0]
tabellone_ratios = [0, 0, 0]
temp_ratios_topleft = [0, 0, 0]
punteggio_home = [0, 0, 0]
punteggio_guest = [0, 0, 0]

#get_names_from_image(match.home_team.name)
#get_names_from_image(match.guest_team.name)
#get_names_from_image("Ref")

print("Done.")

while (capture.isOpened()):
    stime = time.time()
    sicurezza = 0
    ret, frame = capture.read()


    if ret:
        if (temp_num_frame % 3 == 0):
            frame = get_faces(frame)
        # ogni 2 secondi controllo la scena
        if (temp_num_frame == (frame_rate_originale * 2)):

            temp = is_new_scene(frame, old_ratio, True)
            old_ratio[0] = temp[0]
            old_ratio[1] = temp[1]
            old_ratio[2] = temp[2]
            temp_num_frame = 1
            if (temp[3] > .1):
                print("Nuova scena " + str(num_frame))
                num_frame_scena = num_frame

        #DA QUI--------------------------------------------------
            crop = frame[55:70, 225:385]
            cv2.imshow('crop', crop)
            temp2 = is_new_scene(crop, temp_ratios_topleft, False)
            temp_ratios_topleft[0] = temp2[0]
            temp_ratios_topleft[1] = temp2[1]
            temp_ratios_topleft[2] = temp2[2]
            print("temp: " + str(temp2[3]))
            if (tabellone_on):
                distance = count_distance(tabellone_ratios,temp_ratios_topleft)[3]
                print("distanza: "+str(distance))
                temp_ratios_topleft.pop()
                if (distance>0.03):
                    count_event += 1
                    print("è sparito: contiamo: "+str(count_event))
                    if (count_event == 6):
                        print("Evento confermato!")

                        # routine generazione evento
                        event_on = True
                else:
                    print("cartellone riapparso")
                    #routine controllo goal
                    if (event_on):
                        event_on = False
                        crop = frame[55:70, 284:300]
                        cv2.imshow('ita', crop)
                        temp2 = is_new_scene(crop, punteggio_home, False)
                        print("p_h1: "+str(punteggio_home))
                        print("distanza italia: "+str(temp2[3]))
                        if(temp2[3]>0.04):
                            match.home_team.score_goal()
                            print("GOAL ITALIA, FORTISSIMI")
                            punteggio_home[0] = temp2[0]
                            punteggio_home[1] = temp2[1]
                            punteggio_home[2] = temp2[2]
                            print("p_h2: " + str(punteggio_home))
                            #cartellone nuovo
                            crop = frame[55:70, 225:385]
                            temp2 = is_new_scene(crop, temp_ratios_topleft, False)
                            tabellone_ratios[0] = temp2[0]
                            tabellone_ratios[1] = temp2[1]
                            tabellone_ratios[2] = temp2[2]
                        else:
                            crop = frame[55:70, 312:328]
                            cv2.imshow('fra', crop)
                            temp2 = is_new_scene(crop, punteggio_guest, False)
                            print("p_h3: " + str(punteggio_guest))
                            print("distanza francia: " + str(temp2[3]))
                            if (temp2[3] > 0.04):
                                match.guest_team.score_goal()
                                print("GOAL FRANCIA, TANTOVIRIPIGLIAMO")
                                punteggio_guest[0] = temp2[0]
                                punteggio_guest[1] = temp2[1]
                                punteggio_guest[2] = temp2[2]
                                print("p_h4: " + str(punteggio_guest))
                                # cartellone nuovo
                                crop = frame[55:70, 225:385]
                                temp2 = is_new_scene(crop, temp_ratios_topleft, False)
                                tabellone_ratios[0] = temp2[0]
                                tabellone_ratios[1] = temp2[1]
                                tabellone_ratios[2] = temp2[2]
                            else:
                                print("poi vediamo cosa succede qui")
                    count_event = 0

            else:
                if (temp2[3] > 0 and temp2[3] < .02):
                    if (count == 0):
                        current_frame_scena = num_frame_scena
                    count += 1
                    if (count == 5):
                        if (num_frame_scena !=  current_frame_scena):
                            print("C'E' Il TABELLONE")
                            tabellone_ratios[0] = temp_ratios_topleft[0]
                            tabellone_ratios[1] = temp_ratios_topleft[1]
                            tabellone_ratios[2] = temp_ratios_topleft[2]
                            tabellone_on = True
                            #home score
                            crop = frame[55:70, 284:300]
                            cv2.imshow('ita', crop)
                            temp2 = is_new_scene(crop, temp_ratios_topleft, False)
                            punteggio_home[0] = temp2[0]
                            punteggio_home[1] = temp2[1]
                            punteggio_home[2] = temp2[2]
                            print(punteggio_home)
                            #guest score
                            crop = frame[55:70, 312:328]
                            cv2.imshow('fra', crop)
                            temp2 = is_new_scene(crop, temp_ratios_topleft, False)
                            punteggio_guest[0] = temp2[0]
                            punteggio_guest[1] = temp2[1]
                            punteggio_guest[2] = temp2[2]
                            print(punteggio_guest)
                        else:
                            print("Scena non cambiata")
                            count -= 1
                else:
                    print("Azzerato")
                    count = 0
                print ("count: "+str(count))
        #A QUI---------------------------------------------------------------------

        results = tfnet.return_predict(frame)
        for result in results:
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            confidence = result['confidence']
            sicurezza = confidence
            text = '{}: {:.0f}%'.format(label,confidence * 100)
            # ritaglio il bounding box da analizzare
            ymin = int(result['topleft']['y'])
            xmin = int(result['topleft']['x'])
            ymax = int(result['bottomright']['y'])
            xmax = int(result['bottomright']['x'])
            # crop them
            crop_img = frame[ymin:ymax, xmin:xmax]
            color = detect_color(crop_img)
            if "card" in str(label):
                if label == 'red_card':
                    if color == 'not_sure':
                        sicurezza -= .25
                    elif color == 'yellow':
                        sicurezza -= .30
                elif label == 'yellow_card':
                    if color == 'not_sure':
                        sicurezza -= .25
                    elif color == 'red':
                        sicurezza -= .30


            frame = cv2.rectangle(frame, tl, br, (255, 255, 255), 5)
            frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('frame', frame)
        fps = 1 / (time.time() - stime)
        num_frame += 1
        temp_num_frame += 1
        #print('FPS {:.1f}'.format(fps))
        if (time.time() - last_tag_time) > 5:
                if sicurezza > .55:
                    last_tag_time = time.time()
                    event1 = Event(str(datetime.timedelta(seconds=round(num_frame / frame_rate_originale))), label, match.home_team.roster[0])
                    match.event_list.append(event1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        match.json_and_txt_create()
        capture.release()
        cv2.destroyAllWindows()
        break