import os
import time
from datetime import datetime
import multiprocessing

import configs
from cart import Cart
from joystick import JoyStick
from logger import Logger
from widgets import Buzzer
from improved_videocapture import BackgroundVideoCapture


CONTROLLER = JoyStick()
CONTROLLER.open()
CAMERA = BackgroundVideoCapture(configs.FRONT_CAM)
LOGGER = Logger(configs.COLLECTION_SPEED)
BUZZER = Buzzer()

X_AXIS = 0
COUNTER = 0
SUM_CIRCLE = 0

IS_START = False
IS_RESTART = False

while True:
    if IS_RESTART and IS_START:
        LOGGER.log(X_AXIS)
    if IS_RESTART and not IS_START:
        pass
    _, value, type_, number = CONTROLLER.read()
    if CONTROLLER.type(type_) == 'button':
        if number == 6 and value == 1:
            IS_START = True
            IS_RESTART = True
        elif number == 7 and value == 1:
            IS_START = False
            IS_RESTART = False
        elif number == 1 and value == 1:
            IS_START = False
            IS_RESTART = True
    elif CONTROLLER.type(type_) == 'axis':
        print('axis:{} state: {}'.format(number, value))
        if number == 2 and number == 6:
            X_AXIS = value / 32767
