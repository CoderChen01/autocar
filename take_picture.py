import time

import cv2

import config
from widgets import Button
from widgets import Lightwork
from camera import Camera

cam_id = config.front_cam

start_button = Button(1, "UP")
stop_button = Button(1, "DOWN")
cam = Camera(cam_id, width=640, height=480)
counter = 0

if cam == config.front_cam:
    result_dir = './image/front_image'
else:
    result_dir = './image/side_image'

while not start_button.clicked():
    pass

time.sleep(0.2)
Lightwork(2, 'red')
time.sleep(0.2)
Lightwork(2, 'green')
time.sleep(0.2)
Lightwork(2, 'off')
print('Start!')
print('Press the "Down button" to take photos!')

while stop_button.clicked():
    path = "{}/{}.png".format(result_dir, btn)
    counter += 1
    image = camera.read()
    name = "{}.png".format(btn)
    cv2.imwrite(path, image)
camera.release()
