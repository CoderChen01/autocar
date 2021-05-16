import time
from datetime import datetime
import os

import cv2

import configs
from widgets import Button
from tasks import light_work
from improved_videocapture import BackgroundVideoCapture

CAM_ID = configs.FRONT_CAM
IS_TEST = False

start_button = Button(1, 'UP')
stop_button = Button(1, 'DOWN')
pause_button = Button(1, 'LEFT')
cam = BackgroundVideoCapture(CAM_ID)
counter = 0

if CAM_ID == configs.front_cam:
    result_dir = './image/{}_front_image_{}'.format(
        'test' if IS_TEST else 'data',
        datetime.now().strftime('%Y%m%d%H%M%S'))
else:
    result_dir = './image/{}_side_image_{}'.format(
        'test' if IS_TEST else 'data',
        datetime.now().strftime('%Y%m%d%H%M%S'))
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

while not start_button.clicked():
    pass

time.sleep(0.2)
light_work(2, 'red')
time.sleep(0.2)
light_work(2, 'green')
time.sleep(0.2)
light_work(2, 'off')
print('Start!')
print('Press the "Down button" to take photos!')

if not IS_TEST:
    while not stop_button.clicked():
        path = "{}/{}.jpg".format(result_dir, counter)
        counter += 1
        _, image = cam.read()
        name = "{}.jpg".format(counter)
        print(path)
        cv2.imwrite(path, image)
        if pause_button.clicked():
            print('puase, wait to start...')
            time.sleep(2)
            while not pause_button.clicked():
                print('puase, wait to start...')
                pass
else:
    while True:
        start_time = time.time()
        while not start_button.clicked():  # Press the start button to take a photo
            if time.time() - start_time > 10:
                cam.stop()
                exit(0)
        path = "{}/{}.jpg".format(result_dir, counter)
        counter += 1
        image = cam.read()
        name = "{}.jpg".format(counter)
        cv2.imwrite(path, image)
        print(path)
        time.sleep(0.5)
cam.close()
