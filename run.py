import os
import sys
import datetime
import time
import multiprocessing as mp

import cv2
import numpy as np

import configs
from tasks import *
from detectors import SignDetector
from detectors import TaskDetector
from detectors import calculate_area
from widgets import Button
from widgets import Servo, ServoPWM
from cruiser import Cruiser
from driver import Driver
from cart import Cart
from improved_videocapture import BackgroundVideoCapture
from god import God


################## public variables ##################
# flags
SPEED = configs.RUN_SPEED
STATE = 2  # 0 cruise 1 task 2 wait
TASK_ID = 0
FLAG_NUM = 3
TARGET_NUM = 0
IS_FIRST_FLAG = True

# buttons, ultrasonic, cameras
START_BUTTON = Button(1, 'UP')
STOP_BUTTON = Button(1, 'DOWN')
FRON_CAMERA = BackgroundVideoCapture(configs.FRONT_CAM)
SIDE_CAMERA = BackgroundVideoCapture(configs.SIDE_CAM)

# driver
DRIVER = Driver()
DRIVER.set_speed(SPEED)

# detectors
SIGN_DETECTOR = SignDetector()
TASK_DETECTOR = TaskDetector()


################## tools ##################
def is_sign_valid(result):
    """
    Determine whether the target meets the threshold
    """
    x = result.relative_center_x
    y = result.relative_center_y
    area = calculate_area(result.relative_box, result.shape)
    threshold = configs.SIGN_THRESHOLD[result.name]
    return threshold[0][0] < x < threshold[0][1] \
           and threshold[1][0] < y < threshold[1][1] \
           and threshold[2][0] < area < threshold[2][1]


def release_spoil():
    servo = ServoPWM(2)
    servo.servocontrol(90, 100)
    time.sleep(1)


################## stops ##################
def _castle_stop():
    DRIVER.driver_run(15, 15)
    time.sleep(1.5)
    DRIVER.stop()
    time.sleep(1)


def _shot_target_right_stop():
    DRIVER.stop()
    time.sleep(1)
    DRIVER.driver_run(10, 10)
    time.sleep(2.5)
    DRIVER.stop()
    time.sleep(0.5)
    while True:
        grapped, frame = SIDE_CAMERA.read()
        if not grapped:
            exit(-1)
        result = SIGN_DETECTOR.detect(frame)
        x = result.relative_center_x
        y = result.relative_center_y
        x_threshold, y_threshold = configs.TASK_THRESHOLD[TARGET_NUM]
        if x < x_threshold[0]:
            # go forward
            DRIVER.driver_run(10, 10)
            time.sleep(0.5)
            DRIVER.stop()
            time.sleep(0.5)
        elif x > x_threshold[1]:
            # back up
            DRIVER.driver_run(-10, -10)
            time.sleep(0.5)
            DRIVER.stop()
            time.sleep(0.5)
        if y < y_threshold[0]:
            # turn left
            DRIVER.driver_run(0, 10)
            time.sleep(0.5)
            DRIVER.stop()
            time.sleep(0.5)
        elif y > y_threshold[1]:
            # turn right
            DRIVER.driver_run(10, 0)
            time.sleep(0.5)
            DRIVER.stop()
            time.sleep(0.5)
        if x_threshold[0] <= x <= x_threshold[1] \
           and y_threshold[0] <= y <= y_threshold[1]:
           break


def _stop_stop():
    DRIVER.stop()
    time.sleep(1)


def _spoil_left_stop():
    DRIVER.stop()
    time.sleep(1)
    DRIVER.driver_run(10, 10)
    time.sleep(1.5)
    DRIVER.stop()
    time.sleep(1)


def _hay_right_stop():
    DRIVER.stop()
    time.sleep(1)
    DRIVER.driver_run(15, 5)
    time.sleep(1.5)
    DRIVER.stop()
    time.sleep(1)
    DRIVER.driver_run(5, 15)
    time.sleep(1.5)
    DRIVER.stop()
    time.sleep(1)
    DRIVER.driver_run(-10, -10)
    time.sleep(2)
    DRIVER.stop()
    time.sleep(1)


def _end_stop():
    DRIVER.driver_run(10, 10)
    time.sleep(2.5)
    DRIVER.stop()
    time.sleep(1)


################## tasks ##################
def _raise_flag():
    print('raise flag...')
    global IS_FIRST_FLAG
    global FLAG_NUM
    _castle_stop()
    if FLAG_NUM > 5:
        FLAG_NUM = 3
    raise_flag(FLAG_NUM)
    if IS_FIRST_FLAG:
        IS_FIRST_FLAG = False
    FLAG_NUM += 1
    return 0


def _shot_target():
    print('shot target...')
    global TARGET_NUM
    _shot_target_right_stop()
    shot_target()
    TARGET_NUM += 1
    if TARGET_NUM > 2:
        TARGET_NUM = 0
    return 0


def _take_barracks():
    print('take barracks...')
    _stop_stop()
    take_barracks()
    return 0


def _capture_target():
    print('capture target...')
    _spoil_left_stop()
    capture_target()
    time.sleep(1)
    return 0


def _transport_forage():
    print('transport forage...')
    _hay_right_stop()
    transport_forage()
    time.sleep(2)
    return 0


def _end():
    print('end...')
    global IS_FIRST_FLAG
    global FLAG_NUM
    _end_stop()
    release_spoil()
    IS_FIRST_FLAG = True
    FLAG_NUM = 3
    return 2


################## main ##################
def init():
    """
    Initialize operation, lock the servo
    """
    vs1 = Servo(1)
    vs2 = Servo(2)
    vs1.servocontrol(-80, 100)
    time.sleep(0.3)
    vs2.servocontrol(35, 100)
    time.sleep(0.3)


def wait_start_processor():
    global STATE
    buzzing(2)
    for _ in range(30):
        START_BUTTON.clicked()
        STOP_BUTTON.clicked()
    while True:  # wait for starting
        if START_BUTTON.clicked():
            buzzing(3)
            print('init...')
            init()
            print('loading finished...')
            break
        if STOP_BUTTON.clicked():
            SIDE_CAMERA.close()
            FRON_CAMERA.close()
            buzzing(4)
            exit(0)
    print('start operation...')
    STATE = 0


def task_processor():
    print('task...')
    global STATE
    global DRIVER
    task_map = {
        1: _raise_flag,
        2: _shot_target,
        3: _take_barracks,
        4: _capture_target,
        5: _transport_forage,
        6: _end
    }
    STATE = task_map[TASK_ID]()


def cruise_processor():
    print('cruise...')
    global STATE
    global SPEED
    global TASK_ID
    global SIGN_DETECTOR
    while True:
        grabbed, frame = FRON_CAMERA.read()
        DRIVER.go(frame)
        if not grabbed:
            exit(-1)
        result = SIGN_DETECTOR.detect(frame)
        if result and is_sign_valid(result):
            STATE = 1
            TASK_ID = result.index
            break


def run():
    state_map = [cruise_processor, task_processor, wait_start_processor]
    while True:
        state_map[STATE]()


def test_front():
    global FRON_CAMERA
    global SIGN_DETECTOR

    while True:
        _, frame = FRON_CAMERA.read()
        res = SIGN_DETECTOR.detect(frame)
        if not res:
            continue
        print(res.index, res.name, res.relative_center_x, res.relative_center_y)


def test_side():
    while True:
        _, frame = SIDE_CAMERA.read()
        res = TASK_DETECTOR.detect(frame)
        if not res:
            continue
        print(res.index, res.name, res.relative_center_x, res.relative_center_y)


if __name__=='__main__':
    run()
    # _hay_right_stop()