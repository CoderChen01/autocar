import sys
import datetime
import time
import multiprocessing as mp

import cv2

import config
from tasks import *
from detectors import SignDetector
from detectors import TaskDetector
from widgets import Button
from cruiser import Cruiser
from driver import Driver
from cart import Cart
from improved_videocapture import BackgroundVideoCapture


SPEED = config.RUN_SPEED
KX = config.RUN_KX
STATE = 0
TASK_ID = 0
RAISE_FLAG_RECORD = 3

START_BUTTON = Button(1, 'UP')
STOP_BUTTON = Button(1, 'DOWN')

FRON_CAMERA = BackgroundVideoCapture(config.front_cam)
SIDE_CAMERA = BackgroundVideoCapture(config.side_cam)

DRIVER = Driver()
DRIVER.set_speed(SPEED)
DRIVER.set_Kx(KX)

SIGN_DETECTOR = SignDetector()
TASK_DETECTOR = TaskDetector()


def has_sign(sign_result):
    """
    determine if the task is approaching
    """
    if sign_result[1] == -1:
        return False
    return True


def dispatch_task(sign_result):
    """
    set tasks based on the detection
    """
    global TASK_ID
    nearest = sign_result[0][sign_result[1]]  # results[blow_center_index]
    task_id = nearest.index
    if task_id:
        TASK_ID = task_id


def change_state(is_task):
    global STATE
    if is_task:
        STATE = 1
    else:
        STATE = 0


def task_processor():
    print('task...')
    global STATE
    global RAISE_FLAG_RECORD
    grabbed, frame = SIDE_CAMERA.read()
    for _ in range(30):
        if grabbed:
            break
        print('no frame, retrying...')
        grabbed, frame = SIDE_CAMERA.read()
    results = TASK_DETECTOR.detect(frame)
    if TASK_ID == 3:  # raise flag
        raise_flag(RAISE_FLAG_RECORD)
        print('raise flag...')
        RAISE_FLAG_RECORD += 1
    elif TASK_ID == 5:
        shot_target(2)
        print('shot target...')
    elif TASK_ID == 1:
        take_barracks()
        print('take barracks...')
    elif TASK_ID == 2:
        capture_target(1, 2)
        print('capture target...')
    elif TASK_ID == 4:
        transport_forage(1)
        print('transport forage...')
    STATE = 0


def cruise_processor():
    print('cruise...')
    global STATE
    global SPEED
    _has_sign = False
    first_result = None
    while not STOP_BUTTON.clicked():
        grabbed, frame = FRON_CAMERA.read()
        for _ in range(30):
            if grabbed:
                break
            print('no frame, retrying...')
            grabbed, frame = FRON_CAMERA.read()
        DRIVER.go(frame)
        sign_result = SIGN_DETECTOR.detect(frame)
        if not _has_sign and has_sign(sign_result):
            _has_sign = True
            first_result = sign_result
        if _has_sign and not has_sign(sign_result):
            dispatch_task(first_result)
            change_state(True)
            break
    DRIVER.stop()


def run():
    state_map = [cruise_processor, task_processor]
    while not START_BUTTON.clicked():  # wait for starting
        pass
    print('start operation...')
    while not STOP_BUTTON.clicked():
        # wait for stopping
        state_map[STATE]()


if __name__=='__main__':
    run()