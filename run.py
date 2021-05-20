import sys
import datetime
import time
import multiprocessing as mp

import cv2

import configs
from tasks import *
from detectors import SignDetector
from detectors import TaskDetector
from widgets import Button, UltrasonicSensor
from widgets import Servo, ServoPWM
from cruiser import Cruiser
from driver import Driver
from cart import Cart
from improved_videocapture import BackgroundVideoCapture
from god import God


SPEED = configs.RUN_SPEED
KX = configs.RUN_KX
STATE = 0
TASK_ID = 0
IS_FIRST_FLAGE = True


START_BUTTON = Button(1, 'UP')
STOP_BUTTON = Button(1, 'DOWN')
LEFT_ULTRASONICSENSOR = UltrasonicSensor(4)
FRON_CAMERA = BackgroundVideoCapture(configs.FRONT_CAM)
SIDE_CAMERA = BackgroundVideoCapture(configs.SIDE_CAM)

DRIVER = Driver()
DRIVER.set_speed(SPEED)
DRIVER.set_Kx(KX)

TASK_DETECTOR = TaskDetector()
SIGN_DETECTOR = SignDetector()


def init():
    """
    Initialize operation, lock the servo
    """
    time.sleep(4)
    vs1 = Servo(1)
    vs2 = Servo(2)
    s3 = ServoPWM(3)
    s4 = ServoPWM(4)
    s5 = ServoPWM(5)
    vs1.servocontrol(-80, 100)
    time.sleep(1)
    vs2.servocontrol(40, 100)
    time.sleep(1)
    s3.servocontrol(0, 100)
    time.sleep(1)
    s4.servocontrol(0, 100)
    time.sleep(1)
    s5.servocontrol(0, 100)
    time.sleep(1)


def is_valid(x, y, threshold):
    """
    Determine whether the target meets the threshold
    """
    return threshold[0][0] < x < threshold[0][1] \
           and threshold[1][0] < y < threshold[1][1]


def _raise_flag():
    print('raise flag...')
    global DRIVER
    global SIDE_CAMERA
    global TASK_DETECTOR
    global IS_FIRST_FLAGE
    flags = ['dh', 'dj', 'dxj']
    flag_map = {
        'dh': 3,
        'dj': 4,
        'dxj': 5
    }
    flag_threshold = {
        'dh': ((), ()),
        'dj': ((), ()),
        'dxj': ((), ())
    }
    is_scan = False
    DRIVER.driver_run(10, 10)
    time.sleep(1)
    while True:
        distance = LEFT_ULTRASONICSENSOR.read()
        if distance and distance < 30 \
           and not is_scan:
            is_scan = True
        if not is_scan:
            continue
        grabbed, frame = SIDE_CAMERA.read()
        if not grabbed:
            exit(-1)
        results = TASK_DETECTOR.detect(frame)
        if not results:
            distance = LEFT_ULTRASONICSENSOR.read()
            if distance and distance > 30:
                break
            continue
        if results[0].relative_center_x > 0.8 \
           and results[0].name in flags:
            DRIVER.stop()
            time.sleep(1)
            raise_flag(flag_map[results[0].name])
            if IS_FIRST_FLAGE:
                change_camera_direction(2, 'right')
                time.sleep(1)
                IS_FIRST_FLAGE = False
            break


def _shot_target():
    print('shot target...')
    global DRIVER
    global SIDE_CAMERA
    global TASK_DETECTOR
    target = 'target'
    target_threshold = {
        'target': ((0.25, 0.32), (0.35, 0.42))
    }

    DRIVER.driver_run(10, 10)
    time.sleep(1)

    while True:
        grabbed, frame = SIDE_CAMERA.read()
        if not grabbed:
            exit(-1)
        results = TASK_DETECTOR.detect(frame)
        if not results:
            continue
        print(results[0].name)
        if results[0].name == target \
           and is_valid(results[0].relative_center_x,
                        results[0].relative_center_y,
                        target_threshold[results[0].name]):
            DRIVER.stop()
            time.sleep(1)
            shot_target(2)
            break


def _take_barracks():
    take_barracks()
    print('take barracks...')


def _capture_target():
    change_camera_direction(2, 'left')
    time.sleep(1)
    capture_target(1, 2)
    change_camera_direction(2, 'right')
    print('capture target...')


def _transport_forage():
    transport_forage(1)
    change_camera_direction(2, 'left')
    print('transport forage...')


def task_processor():
    print('task...')
    global STATE
    global DRIVER
    task_map = {
        1: _raise_flag,
        2: _shot_target,
        3: _take_barracks,
        4: _capture_target,
        5: _transport_forage
    }
    DRIVER.stop()
    time.sleep(1)
    task_map[TASK_ID]()
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
    init()
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