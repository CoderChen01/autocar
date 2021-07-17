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
from distance import Distance


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
# cruise predictor weights
CRUISE_PREDICTOR_WEIGHTS = (0.6, 0.4)
# IS_FIRST_FLAG = True
HAS_STOPPED = False
HAS_CAPTURE = False
HAS_TRANSPORT = False
FINISH_FLAG = False

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


def finetune(threshold=configs.FINETUNE_THRESHOLD):
    fintune_count = 0
    while True:
        all_result = 0
        for _ in range(10):
            grapped, frame = FRON_CAMERA.read()
            if not grapped:
                exit(-1)
            result = DRIVER.cruiser.cruise(frame)
            all_result += result
        avg_result= all_result / 10
        abs_avg_result = abs(avg_result)
        if abs_avg_result < threshold:
            break
        if avg_result < 0:
            fintune_count += 0.2
            DRIVER.driver_run(0, 15, 0.2)
        elif avg_result > 0:
            fintune_count += 0.2
            DRIVER.driver_run(15, 0, 0.2)
    return fintune_count


################## stops ##################
def _castle_stop():
    DRIVER.driver_run(15, 15, 1.5)


def _shot_target_right_stop():
    DRIVER.stop()
    finetune_time = finetune()
    interval = 1.5 - finetune_time
    if interval > 0:
        DRIVER.driver_run(10, 10, interval)
    none_count = 0
    while True:
        grapped, frame = SIDE_CAMERA.read()
        if not grapped:
            exit(-1)
        result = TASK_DETECTOR.detect(frame)
        x_threshold, area_threshold = configs.TASK_THRESHOLD[TARGET_NUM]
        if not result or \
           not area_threshold[0] < calculate_area(result.relative_box, result.shape) < area_threshold[1]:
            none_count += 1
            if none_count >= 18:
                break
            if none_count < 5:
                DRIVER.driver_run(10, 10, 1)
            elif 10 >= none_count >= 5:
                DRIVER.driver_run(-10, -10, 1)
            elif 12 >= none_count > 10:
                DRIVER.driver_run(0, 10, 0.5)
                DRIVER.driver_run(10, 0, 0.5)
            elif 15 >= none_count > 12:
                DRIVER.driver_run(10, 10, 0.5)
            else:
                DRIVER.driver_run(-10, -10, 1)
            continue
        x = result.relative_center_x
        y = result.relative_center_y
        if x < x_threshold[0]:
            # go forward
            DRIVER.driver_run(10, 10, abs(x - x_threshold[0]))
        elif x > x_threshold[1]:
            # back up
            DRIVER.driver_run(-10, -10, abs(x - x_threshold[1]))
        if x_threshold[0] <= x <= x_threshold[1]:
           break


def _stop_stop():
    DRIVER.stop()
    finetune_time = finetune()
    interval = 1.5 - finetune_time
    if interval > 0:
        DRIVER.driver_run(10, 10, interval)


def _spoil_stop():
    DRIVER.stop()
    DRIVER.driver_run(10, 10, 1.5)


def _hay_right_stop():
    DRIVER.stop()
    finetune()
    # cruise finetune
    all_result = 0
    for _ in range(10):
        grapped, frame = FRON_CAMERA.read()
        if not grapped:
            exit(-1)
        result = DRIVER.cruiser.cruise(frame)
        all_result += result
    avg_result= all_result / 10
    if avg_result > -0.035:
        while True:
            all_result = 0
            DRIVER.driver_run(15, 15 * 0.3, 0.5)
            DRIVER.driver_run(15 * 0.3, 15, 0.5)
            for _ in range(10):
                grapped, frame = FRON_CAMERA.read()
                if not grapped:
                    exit(-1)
                result = DRIVER.cruiser.cruise(frame)
                all_result += result
            avg_result = all_result / 10
            if avg_result <= -0.035:
                break


def _end_stop():
    DRIVER.driver_run(10, 10, 2.5)


################## tasks ##################
def _raise_flag():
    global FLAG_NUM
    global FINISH_FLAG
    print('raise flag...')
    _castle_stop()
    if FLAG_NUM > 5:
        FLAG_NUM = 3
    raise_flag(FLAG_NUM)
    if FLAG_NUM == 5:
        FINISH_FLAG = True
    FLAG_NUM += 1
    return 0


def _shot_target():
    global STATE
    global TASK_ID
    global FLAG_NUM
    global TARGET_NUM
    print('shot target...')
    if FLAG_NUM != 5:
        FLAG_NUM = 5
    _shot_target_right_stop()
    shot_target()
    TARGET_NUM += 1
    if TARGET_NUM > 2:
        TARGET_NUM = 0
    return 0


def _take_barracks():
    global HAS_STOPPED
    if HAS_STOPPED or HAS_TRANSPORT \
            or HAS_CAPTURE or FINISH_FLAG:
        return 0
    print('take barracks...')
    _stop_stop()
    take_barracks(DRIVER)
    HAS_STOPPED = True
    return 0


def _capture_target():
    global HAS_CAPTURE
    global CRUISE_PREDICTOR_WEIGHTS
    CRUISE_PREDICTOR_WEIGHTS = (0.3, 0.7)
    if HAS_CAPTURE or HAS_TRANSPORT or FINISH_FLAG:
        return 0
    print('capture target...')
    _spoil_stop()
    capture_target()
    HAS_CAPTURE = True
    return 0


def _transport_forage():
    global HAS_TRANSPORT
    if HAS_TRANSPORT or FINISH_FLAG:
        return 0
    print('transport forage...')
    _hay_right_stop()
    transport_forage()
    HAS_TRANSPORT = True
    return 0


def _end():
    global HAS_STOPPED
    global HAS_CAPTURE
    global HAS_TRANSPORT
    global FLAG_NUM
    global FINISH_FLAG
    if not FINISH_FLAG:
        return 0
    HAS_STOPPED = False
    HAS_CAPTURE = False
    HAS_TRANSPORT = False
    FINISH_FLAG = False
    FLAG_NUM = 3
    _end_stop()
    release_spoil()
    return 2


################## main ##################
def init():
    """
    Initialize operation, lock the servo
    """
    global CRUISE_PREDICTOR_WEIGHTS
    CRUISE_PREDICTOR_WEIGHTS = (0.6, 0.4)
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
    buzzing(2, 0.3)
    for _ in range(30):
        START_BUTTON.clicked()
        STOP_BUTTON.clicked()
    while True:  # wait for starting
        if START_BUTTON.clicked():
            buzzing(3, 0.3)
            print('init...')
            init()
            print('loading finished...')
            break
        if STOP_BUTTON.clicked():
            SIDE_CAMERA.close()
            FRON_CAMERA.close()
            buzzing(4, 0.3)
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
        DRIVER.go(frame, CRUISE_PREDICTOR_WEIGHTS)
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
        print(res.index, res.name, res.score)


def test_cruise():
    while True:
        _, frame = FRON_CAMERA.read()
        start_time = time.time()
        res1 = DRIVER.cruiser.cruise(frame, 0)
        res2 = DRIVER.cruiser.cruise(frame, 1)
        print(time.time() - start_time)
        print(res1, res2)


if __name__=='__main__':
    # run()
    # finetune()
    # cruise_processor()
    # DRIVER.cart.steer(0.3)
    # time.sleep(10)
    # test_cruise()
    # _transport_forage()
    # finetune()
    # _shot_target_right_stop()
    _hay_right_stop()
    # test_front()
    # test_side()
    # _take_barracks()
