import os
import time
from datetime import datetime
import multiprocessing

import configs
from cart import Cart
from joystick import JoyStick
from serial_logger import Logger
from widgets import Buzzer, Servo


LOGGER = Logger(configs.COLLECTION_SPEED)
BUZZER = Buzzer()
CONTROLLER = JoyStick()
CONTROLLER.open()

time.sleep(4)
s = Servo(1)
s.servocontrol(-80, 100)

X_AXIS = 0
COUNTER = 0
SUM_CIRCLE = 0

IS_START = False

while True:
    _, value, type_, number = CONTROLLER.read()
    if CONTROLLER.type(type_) == 'button':
        if number == 6 and value == 1:
            LOGGER.start()
            IS_START = True
        elif number == 7 and value == 1:
            IS_START = False
            LOGGER.stop()
            break
        elif number == 1 and value == 1:
            IS_START = False
            COUNTER = LOGGER.counter
            LOGGER.stop()
            del LOGGER
            LOGGER = Logger(configs.COLLECTION_SPEED)
            LOGGER.counter = COUNTER
            SUM_CIRCLE += 1
            if SUM_CIRCLE == configs.SUM_CIRCLE:
                for _ in range(3):
                    BUZZER.rings()
                    time.sleep(1)
    elif CONTROLLER.type(type_) == 'axis':
        if number == 6:
            X_AXIS = value / 32767

    if IS_START:
        LOGGER.log(X_AXIS)
