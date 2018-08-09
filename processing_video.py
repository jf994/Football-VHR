import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import datetime
from create_json import writeToJSONFile

option = {
    'model': 'cfg/tiny-yolo-voc-2c.cfg',
    'load': 3375,
    'threshold': 0.15,
    'gpu': 1.0
}

frame_rate_originale = 29.88
tfnet = TFNet(option)
last_tag_time = 0
capture = cv2.VideoCapture('video_cards2.mp4')
colors = [tuple(255 * np.random.rand(3)) for i in range(5)]
num_frame = 0

while (capture.isOpened()):
    stime = time.time()
    sicurezza = 0
    ret, frame = capture.read()
    if ret:
        results = tfnet.return_predict(frame)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            confidence = result['confidence']
            sicurezza = confidence
            text = '{}: {:.0f}%'.format(label,confidence * 100)
            frame = cv2.rectangle(frame, tl, br, color, 5)
            frame = cv2.putText(frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        fps = 1 / (time.time() - stime)
        num_frame += 1
        print('FPS {:.1f}'.format(fps))
        if (time.time() - last_tag_time) > 5:
            if sicurezza > .15:
                last_tag_time = time.time()
                data = {}
                data['event'] = label
                data['time_sec'] = round(num_frame/frame_rate_originale)
                data['time_hh:mm:ss'] = str(datetime.timedelta(seconds=round(num_frame / frame_rate_originale)))
                writeToJSONFile('json', str(label)+"_"+str(round(num_frame/frame_rate_originale)), data)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        capture.release()
        cv2.destroyAllWindows()
        break