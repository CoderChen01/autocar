import time
from datetime import datetime
import os

import cv2

import config
from widgets import Button
from tasks import light_work
from camera import Camera

CAM_ID = config.front_cam
IS_TEST = True

start_button = Button(1, "UP")
stop_button = Button(1, "DOWN")
cam = Camera(CAM_ID, width=640, height=480)
counter = 0

if CAM_ID == config.front_cam:
    result_dir = './image/{}_front_image_{}'.format(
        'test' if IS_TEST else 'data',
        datetime.now().strftime('%Y%m%d%H%M%S'))
else:
    result_dir = './image/side_image_{}'.format(
        'test' if IS_TEST else 'data',
        datetime.now().strftime('%Y%m%d%H%M%S'))
if os.path.exists(result_dir):
    os.makedirs(result_dir)

while not start_button.clicked():
    pass

cam.start()
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
        path = "{}/{}.png".format(result_dir, counter)
        counter += 1
        image = cam.read()
        name = "{}.png".format(counter)
        print(path)
        cv2.imwrite(path, image)
else:
    while True:
        start_time = time.time()
        while not start_button.clicked():  # Press the start button to take a photo
            if time.time() - start_time > 10:
                exit(0)
                cam.stop()
        path = "{}/{}.png".format(result_dir, counter)
        counter += 1
        image = cam.read()
        name = "{}.png".format(counter)
        cv2.imwrite(path, image)
cam.stop()
