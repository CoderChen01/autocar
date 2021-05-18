import sys
import datetime
import time
import multiprocessing as mp

import cv2

import configs
from tasks import *
from detectors import SignDetector
from detectors import TaskDetector
from widgets import Button
from cruiser import Cruiser
from driver import Driver
from cart import Cart
from improved_videocapture import BackgroundVideoCapture
from god import God


SPEED = configs.RUN_SPEED
KX = configs.RUN_KX
STATE = 0
TASK_ID = 0
RAISE_FLAG_RECORD = 3


START_BUTTON = Button(1, 'UP')
STOP_BUTTON = Button(1, 'DOWN')

FRON_CAMERA = BackgroundVideoCapture(configs.FRONT_CAM)
SIDE_CAMERA = BackgroundVideoCapture(configs.SIDE_CAM)

DRIVER = Driver()
DRIVER.set_speed(SPEED)
DRIVER.set_Kx(KX)

TASK_DETECTOR = TaskDetector()
SIGN_DETECTOR = SignDetector()


def task_processor():
    print('task...')
    global STATE
    global RAISE_FLAG_RECORD
    global DRIVER
    DRIVER.stop()
    grabbed, frame = SIDE_CAMERA.read()
    if not grabbed:
        exit(-1)
    results = TASK_DETECTOR.detect(frame)
    if TASK_ID == 1:  # raise flag
        if RAISE_FLAG_RECORD == 6:
            RAISE_FLAG_RECORD = 3
        raise_flag(RAISE_FLAG_RECORD)
        print('raise flag...')
        RAISE_FLAG_RECORD += 1
    elif TASK_ID == 2:
        shot_target(2)
        print('shot target...')
    elif TASK_ID == 3:
        take_barracks()
        print('take barracks...')
    elif TASK_ID == 4:
        capture_target(1, 2)
        print('capture target...')
    elif TASK_ID == 5:
        transport_forage(1)
        print('transport forage...')
    time.sleep(1)
    STATE = 0


def cruise_processor():
    print('cruise...')
    global STATE
    global SPEED
    global TASK_ID
    global SIGN_DETECTOR
    while True:
        grabbed, frame = FRON_CAMERA.read()
        if not grabbed:
            exit(-1)
        DRIVER.go(frame)
        results = SIGN_DETECTOR.detect(frame)
        if not results:
            STATE = 0
            TASK_ID = 0
            continue
        STATE = 1
        TASK_ID = results[0].index
        break


def run():
    global FRON_CAMERA
    global SIDE_CAMERA
    state_map = [cruise_processor, task_processor]
    while not START_BUTTON.clicked():  # wait for starting
        pass
    print('start operation...')
    while True:
        # wait for stopping
        state_map[STATE]()
    # FRON_CAMERA.close()
    # SIDE_CAMERA.close()


if __name__=='__main__':
    run()