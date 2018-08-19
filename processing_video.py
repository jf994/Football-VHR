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
do_switch = [0, 0]
events = 0
old_ratio = [0, 0, 0]
old_ratios_punteggio = [[0, 0, 0], [0, 0, 0]]
saved_ratios_punteggio = [[-1, -1, -1], [-1, -1, -1]]

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
        if (temp_num_frame == (frame_rate_originale)):

            temp = is_new_scene(frame, old_ratio, True)
            old_ratio[0] = temp[0]
            old_ratio[1] = temp[1]
            old_ratio[2] = temp[2]
            temp_num_frame = 1
            if (temp[3] > .1):
                print("Nuova scena " + str(num_frame))
                num_frame_scena = num_frame

            #crop = frame[55:70, 305:335]
            crops = []
            crops.append(frame[55:70, 275:305])
            crops.append(frame[55:70, 305:335])

            for (i, crop) in enumerate(crops):
                #cv2.imshow('crop', crop)
                temp2 = is_new_scene(crop, old_ratios_punteggio[i], False)
                old_ratios_punteggio[i][0] = temp2[0]
                old_ratios_punteggio[i][1] = temp2[1]
                old_ratios_punteggio[i][2] = temp2[2]
                if (temp2[3] < .05):
                    do_switch[i] += 1
                    if (do_switch[i] == 10):
                        if (current_frame_scena == num_frame_scena):
                            do_switch[0] = 0
                            do_switch[1] = 0
                        else:
                            count_distance(saved_ratios_punteggio[i], old_ratios_punteggio[i])
                            print(" diff: " + str(old_ratios_punteggio[i][3]))
                            events += 1
                            saved_ratios_punteggio[i][0] = old_ratios_punteggio[i][0]
                            saved_ratios_punteggio[i][1] = old_ratios_punteggio[i][1]
                            saved_ratios_punteggio[i][2] = old_ratios_punteggio[i][2]
                            if (old_ratios_punteggio[i][3] > .05):
                                print("GOOOOOOOOOOOOOOOOOOOOAAAAAAAAAAAAAAL")
                                match.home_team.score_goal()
                            old_ratios_punteggio[i].pop()

                else:
                    do_switch[0] = 0
                    do_switch[1] = 0
                    current_frame_scena = num_frame_scena

            print(str(do_switch[0]) + " - " + str(do_switch[1]))

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