import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import datetime
from create_json import writeToJSONFile
from get_color import detect_team

option = {
    'model': 'cfg/tiny-yolo-voc-2c.cfg',
    'load': 2875,
    'threshold': 0.5,
    'gpu': 1.0
}

frame_rate_originale = 25
tfnet = TFNet(option)
last_tag_time = 0
capture = cv2.VideoCapture('final2006_short.mp4')
num_frame = 0

while (capture.isOpened()):
    stime = time.time()
    sicurezza = 0
    ret, frame = capture.read()
    if ret:
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
            color = detect_team(crop_img)
            if "card" in str(label):
                if color == 'red' and label == 'red_card':
                    label = 'red_card'
                elif color == 'yellow' and label == 'yellow_card':
                    label = 'yellow_card'
                else:
                    sicurezza = 0
            if (time.time() - last_tag_time) > 5:
                if sicurezza > .5:
                    frame = cv2.rectangle(frame, tl, br, (255,255,255), 5)
                    frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('frame', frame)
        fps = 1 / (time.time() - stime)
        num_frame += 1
        #print('FPS {:.1f}'.format(fps))
        if (time.time() - last_tag_time) > 5:
                if sicurezza > .5:
                    last_tag_time = time.time()
                    data = {}
                    data['event'] = label
                    data['time_sec'] = round(num_frame/frame_rate_originale)
                    data['time_hh:mm:ss'] = str(datetime.timedelta(seconds=round(num_frame / frame_rate_originale)))
                    data['confidence'] = str(sicurezza * 100)+"%"
                    writeToJSONFile('json', str(label)+"_"+str(round(num_frame/frame_rate_originale)), data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        capture.release()
        cv2.destroyAllWindows()
        break