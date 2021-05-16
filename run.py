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
STATE = mp.Value('i', 0)
TASK_ID = mp.Value('i', 0)
FRAME_QUEUE = mp.Queue()
LOCK = mp.Lock()
RAISE_FLAG_RECORD = 3


START_BUTTON = Button(1, 'UP')
STOP_BUTTON = Button(1, 'DOWN')

FRON_CAMERA = BackgroundVideoCapture(config.front_cam)
SIDE_CAMERA = BackgroundVideoCapture(config.side_cam)

DRIVER = Driver()
DRIVER.set_speed(SPEED)
DRIVER.set_Kx(KX)

TASK_DETECTOR = TaskDetector()


def task_processor():
    print('task...')
    global STATE
    global RAISE_FLAG_RECORD
    global DRIVER
    time.sleep(1.5)
    DRIVER.stop()
    grabbed, frame = SIDE_CAMERA.read()
    for _ in range(30):
        if grabbed:
            break
        print('no frame, retrying...')
        grabbed, frame = SIDE_CAMERA.read()
    if not grabbed:
        exit(-1)
    results = TASK_DETECTOR.detect(frame)
    if TASK_ID.value == 3:  # raise flag
        raise_flag(RAISE_FLAG_RECORD)
        print('raise flag...')
        RAISE_FLAG_RECORD += 1
    elif TASK_ID.value == 5:
        shot_target(2)
        print('shot target...')
    elif TASK_ID.value == 1:
        take_barracks()
        print('take barracks...')
    elif TASK_ID.value == 2:
        capture_target(1, 2)
        print('capture target...')
    elif TASK_ID.value == 4:
        transport_forage(1)
        print('transport forage...')
    STATE.value = 0


def cruise_processor():
    print('cruise...')
    global STATE
    global SPEED
    global FRAME_QUEUE
    global LOCK
    while not STOP_BUTTON.clicked():
        grabbed, frame = FRON_CAMERA.read()
        for _ in range(30):
            if grabbed:
                break
            print('no frame, retrying...')
            grabbed, frame = FRON_CAMERA.read()
        if not grabbed:
            exit(-1)
        with LOCK:
            DRIVER.go(frame)
        FRAME_QUEUE.put(frame)
        if STATE.value:
            break


def sign_sub_processor():
    global STATE
    global FRAME_QUEUE
    sign_detector = SignDetector()
    while True:
        if STATE.value:
            continue
        if FRAME_QUEUE.qsize() == 0:
            continue
        while FRAME_QUEUE.qsize() > 1:
            FRAME_QUEUE.get()
        frame = FRAME_QUEUE.get()
        with LOCK:
            results, blow_index = sign_detector.detect(frame)
        if not results:
            TASK_ID.value = 0
            STATE.value = 0
            continue
        TASK_ID.value = results[blow_index].index
        STATE.value = 1


def run():
    global FRON_CAMERA
    global SIDE_CAMERA
    state_map = [cruise_processor, task_processor]
    while not START_BUTTON.clicked():  # wait for starting
        pass
    print('start operation...')
    sign_sub = mp.Process(target=sign_sub_processor)
    sign_sub.daemon = True
    sign_sub.start()
    while not STOP_BUTTON.clicked():
        # wait for stopping
        state_map[STATE.value]()
    FRON_CAMERA.close()
    SIDE_CAMERA.close()


if __name__=='__main__':
    run()