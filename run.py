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


################## public variables ##################
# flags
SPEED = configs.RUN_SPEED
# 0 cruise 1 task 2 wait
STATE = 2
# record task id
TASK_ID = 0
# record the next flag num
FLAG_NUM = 3
# record the target flag num
TARGET_NUM = 0
# record whether the flag is raised for the first time
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
    DRIVER.driver_run(15, 15, 1.5)


def _shot_target_right_stop():
    DRIVER.stop()
    DRIVER.driver_run(10, 10, 2.5)
    none_count = 0
    last_action = None
    while True:
        grapped, frame = SIDE_CAMERA.read()
        if not grapped:
            exit(-1)
        result = TASK_DETECTOR.detect(frame)
        x_threshold, y_threshold, area_threshold = configs.TASK_THRESHOLD[TARGET_NUM]
        if not result or \
           not area_threshold[0] < calculate_area(result.relative_box, result.shape) < area_threshold[1]:
            none_count += 1
            if none_count >= 10:
                break
            if not last_action and none_count < 5:
                DRIVER.driver_run(10, 10, 0.3)
            elif not last_action and none_count >= 5:
                DRIVER.driver_run(-10, -10, 0.3)
            if last_action == 'forward':
                DRIVER.driver_run(-10, -10, 0.2)
            elif last_action == 'back':
                DRIVER.driver_run(10, 10, 0.2)
            elif last_action == 'left':
                DRIVER.turn_right_cm(0.3)
            elif last_action == 'right':
                DRIVER.turn_left_cm(0.3)
            continue
        x = result.relative_center_x
        y = result.relative_center_y
        if x < x_threshold[0]:
            # go forward
            DRIVER.driver_run(10, 10, 0.3)
            last_action = 'forward'
        elif x > x_threshold[1]:
            # back up
            DRIVER.driver_run(-10, -10, 0.3)
            last_action = 'back'
        if y < y_threshold[0]:
            # turn left
            DRIVER.turn_left_cm(0.5)
            last_action = 'left'
        elif y > y_threshold[1]:
            # turn right
            DRIVER.turn_right_cm(0.5)
            last_action = 'right'
        if x_threshold[0] <= x <= x_threshold[1] \
           and y_threshold[0] <= y <= y_threshold[1]:
           break


def _stop_stop():
    DRIVER.stop()
    DRIVER.driver_run(-10, -10, 1.5)


def _spoil_left_stop():
    DRIVER.stop()
    DRIVER.driver_run(10, 10, 1.5)


def _hay_right_stop():
    DRIVER.stop()
    DRIVER.turn_right_cm(2)


def _end_stop():
    DRIVER.driver_run(10, 10, 2.5)


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
    global STATE
    global TASK_ID
    _shot_target_right_stop()
    shot_target()
    TARGET_NUM += 1
    if TARGET_NUM == 1:
        DRIVER.set_speed(25)
        while True:
            grabbed, frame = FRON_CAMERA.read()
            if not grabbed:
                exit(-1)
            DRIVER.go(frame)
            result = SIGN_DETECTOR.detect(frame)
            if result and is_sign_valid(result):
                TASK_ID = result.index
                DRIVER.set_speed(configs.RUN_SPEED)
                return 1
    elif TARGET_NUM > 2:
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
    return 0


def _transport_forage():
    print('transport forage...')
    _hay_right_stop()
    transport_forage()
    DRIVER.turn_left_cm(2)
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
    servo2 = ServoPWM(2)
    vs1.servocontrol(-80, 100)
    time.sleep(0.3)
    vs2.servocontrol(35, 100)
    time.sleep(0.3)
    servo2.servocontrol(180, 100)
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
    global TASK_ID
    global SIGN_DETECTOR
    while True:
        grabbed, frame = FRON_CAMERA.read()
        if not grabbed:
            exit(-1)
        DRIVER.go(frame)
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
        print(is_sign_valid(res), res.name, res.relative_center_x, res.relative_center_y)


def test_side():
    x_threshold, y_threshold, area_threshold = configs.TASK_THRESHOLD[TARGET_NUM]
    while True:
        _, frame = SIDE_CAMERA.read()
        res = TASK_DETECTOR.detect(frame)
        if not res:
            continue
        s = calculate_area(res.relative_box, res.shape)
        print(res.index, res.name, res.score, s)


if __name__=='__main__':
    run()
    # finetune()
    # _shot_target_right_stop()
    # _hay_right_stop()
    # test_front()
    # test_side()
