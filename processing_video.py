import cv2
import sys
from darkflow.net.build import TFNet
import numpy as np
import time
import datetime
from oologic.event import Event
from get_color import detect_color
from get_scene_change import is_new_scene,count_distance
from face_rec import get_faces, get_names_from_image
from oologic.create_test_match import createMatch
from oologic.person import Person
from get_options import get_opt
from count_white_pixels import count_difference_white


def assign_vector(vector, vector_temp):
        for i in range(0, 3):
            vector[i] = vector_temp[i]

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
count_tabellone_on = 0
are_even = 0
crop_old_home = 0
crop_old_guest = 0
event_on = False
tabellone_on = False
old_ratio = [0, 0, 0]
tabellone_ratios = [0, 0, 0]
temp_ratios_topleft = [0, 0, 0]
unknown_person = Person('Unknown', '')

get_names_from_image(match.home_team.name)
get_names_from_image(match.guest_team.name)
get_names_from_image("Ref")

print("Done.")

while (capture.isOpened()):
    stime = time.time()
    sicurezza = 0
    ret, frame = capture.read()

    if ret:
        #controllo le facce ogni 3 frame
        if(temp_num_frame % 3 == 0):
            frame = get_faces(frame)
        # ogni 2 secondi controllo la scena e il risultato
        if(temp_num_frame == (frame_rate_originale * 2)):
            #calcolo ratio e variazione valori RGB per controllare cambio scena
            temp_scene = is_new_scene(frame, old_ratio, True)
            assign_vector(old_ratio, temp_scene)
            temp_num_frame = 1
            #verifico l'avvenuto cambio di scena
            if(temp_scene[3] > .1):
                num_frame_scena = num_frame

            #ritaglio il frame dove dovrebbe essere il tabellone col risultato
            crop = frame[55:70, 225:385]
            temp_topleft = is_new_scene(crop, temp_ratios_topleft, False)
            assign_vector(temp_ratios_topleft, temp_topleft)
            #se il tabellone è già stato trovato...
            if (tabellone_on):
                #...verifico se è ancora presente o meno...
                #print("tab_ratios")
                #print(tabellone_ratios)
                distance = count_distance(tabellone_ratios, temp_ratios_topleft)[3]
                temp_ratios_topleft.pop()
                print("distance: "+str(distance))
                #...se è assente...
                if (distance>0.03):
                    #...conto
                    count_event += 1
                    #...arrivati a 12 secondi di assenza (6 * 2 volte il frame rate)...
                    if (count_event == 6):
                        #confermo l'avvenuto evento
                        event_on = True
                        count_tabellone_on = 0
                        current_frame_scena = num_frame_scena
                        print("C'è un evento.")

                    #dopo 3 minuti e 20 secondi di assenza del tabellone, assumiamo la fine del tempo
                    elif (count_event == 100):
                        event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                           (count_event * 2)))),
                                      'End first half',
                                      unknown_person)
                        match.event_list.append(event)
                elif(distance <= 0.03 and count_tabellone_on == 2 and num_frame_scena !=  current_frame_scena):
                    #riappare il tabellone, controllo che tipo di evento è avvenuto
                    print("count_event: "+str(count_event))
                    if (event_on):
                        print("Nuovo evento.")
                        event_on = False
                        crop_h = frame[55:70, 284:300]
                        crop_g = frame[55:70, 312:328]
                        diff_crop = count_difference_white(crop_h, crop_g, crop_old_home, crop_old_guest)
                        if(are_even <= 0 and diff_crop == -1) or (are_even == 1 and diff_crop == 0) or (are_even > 1 and diff_crop == -1):
                            are_even -= 1
                            match.home_team.score_goal()
                            event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                               (count_event * 2)))),
                                          'Goal '+str(match.home_team.name),
                                          unknown_person)
                            match.event_list.append(event)
                            print("GOAL ITALIA")
                            crop_old_home = frame[55:70, 284:300]
                            #memorizzo le nuove ratio del tabellone cambiato
                            crop = frame[55:70, 225:385]
                            temp_topleft = is_new_scene(crop, temp_ratios_topleft, False)
                            assign_vector(tabellone_ratios, temp_topleft)
                        elif(are_even >= 0 and diff_crop == 1) or (are_even == -1 and diff_crop == 0) or (are_even < -1 and diff_crop == 1):
                            are_even += 1
                            match.guest_team.score_goal()
                            print("tempo: "+str(num_frame / frame_rate_originale))
                            print("meno: "+str(count_event * 2))
                            event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                               (count_event * 2)))),
                                           'Goal '+str(match.guest_team.name),
                                           unknown_person)
                            match.event_list.append(event)
                            print("GOAL FRANCIA")
                            crop_old_guest = frame[55:70, 312:328]
                            # memorizzo le nuove ratio del tabellone cambiato
                            crop = frame[55:70, 225:385]
                            temp_topleft = is_new_scene(crop, temp_ratios_topleft, False)
                            assign_vector(tabellone_ratios, temp_topleft)
                        else:
                            #altrimenti evento sconosciuto
                            print("Mini spot")
                            event = Event(str(datetime.timedelta(seconds=round((num_frame / frame_rate_originale) -
                                                                               (count_event * 2)))),
                                           'Unknown Event',
                                           unknown_person)
                            match.event_list.append(event)
                    count_event = 0
                elif(distance <= 0.03 and count_tabellone_on != 2):
                    if(num_frame_scena !=  current_frame_scena):
                        count_tabellone_on += 1
            #se il tabellone non è ancora stato trovato...
            else:
                #...nel caso in cui si rilevi una variazione minima...
                if(temp_topleft[3] > 0 and temp_topleft[3] < .02):
                    #...inizio a contare e (nel caso sia il primo giro) salvo la scena attuale
                    if(count == 0):
                        current_frame_scena = num_frame_scena
                    count += 1
                    #dopo 10 secondi senza variazioni significative...
                    if(count == 5):
                        #controllo che ci sia stato almeno un cambio di scena
                        if(num_frame_scena !=  current_frame_scena):
                            #confermo la presenza del cartellone e salvo le varie ratio
                            print("C'E' Il TABELLONE")
                            crop_old_home = frame[55:70, 284:300]
                            crop_old_guest = frame[55:70, 312:328]
                            assign_vector(tabellone_ratios, temp_ratios_topleft)
                            tabellone_on = True
                        else:
                            #se la scena non è cambiata, decremento count e ricontrollo
                            count -= 1
                else:
                    #se ho ottenuto una variazione eccessiva, azzero count
                    count = 0

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
                        sicurezza -= .30
                    elif color == 'yellow':
                        sicurezza -= .35
                elif label == 'yellow_card':
                    if color == 'not_sure':
                        sicurezza -= .30
                    elif color == 'red':
                        sicurezza -= .35

            if sicurezza > .55:
                frame = cv2.rectangle(frame, tl, br, (255, 255, 255), 5)
                frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('frame', frame)
        fps = 1 / (time.time() - stime)
        num_frame += 1
        temp_num_frame += 1
        #print('FPS {:.1f}'.format(fps))
        if (time.time() - last_tag_time) > 5:
                if sicurezza > .55:
                    print("Ho salvato "+str(label)+" con sicurezza: "+str(sicurezza*100)+"%")
                    last_tag_time = time.time()
                    event = Event(str(datetime.timedelta(seconds=round(num_frame / frame_rate_originale))), label, unknown_person)
                    match.event_list.append(event)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        match.json_and_txt_create()
        capture.release()
        cv2.destroyAllWindows()
        break