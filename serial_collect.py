import os
import time
from datetime import datetime
import multiprocessing

import configs
from cart import Cart
from joystick import JoyStick
from serial_logger import Logger
from widgets import Buzzer


LOGGER = Logger(configs.COLLECTION_SPEED)
BUZZER = Buzzer()
CONTROLLER = JoyStick()
CONTROLLER.open()
time.sleep(2)

X_AXIS = 0
COUNTER = 0
SUM_CIRCLE = 0

IS_FIRST = True
IS_START = False
IS_RESTART = False

while True:
    _, value, type_, number = CONTROLLER.read()
    if CONTROLLER.type(type_) == 'button':
        if number == 6 and value == 1:
            LOGGER.start()
            IS_START = True
            IS_RESTART = True
            IS_FIRST = False
        elif number == 7 and value == 1:
            IS_START = False
            IS_RESTART = False
            IS_FIRST = False
        elif number == 1 and value == 1:
            IS_START = False
            IS_RESTART = True
            SUM_CIRCLE += 1
            if SUM_CIRCLE == configs.SUM_CIRCLE:
                for _ in range(3):
                    BUZZER.rings()
                    time.sleep(1)
    elif CONTROLLER.type(type_) == 'axis':
        if number == 6:
            X_AXIS = value / 32767

    if not IS_FIRST and IS_RESTART and IS_START:
        LOGGER.log(X_AXIS)
    elif not IS_FIRST and IS_RESTART and not IS_START:
        IS_FIRST = True
        COUNTER = LOGGER.counter
        LOGGER.stop()
        del LOGGER
        LOGGER = Logger(configs.COLLECTION_SPEED)
        LOGGER.counter = COUNTER
    elif not IS_FIRST and not IS_RESTART:
        LOGGER.stop()
        break