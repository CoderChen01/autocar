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
STATE = 2
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
    DRIVER.driver_run(10, 10)
    time.sleep(1)
    while True:
        grabbed, frame = SIDE_CAMERA.read()
        if not grabbed:
            exit(-1)
        result = TASK_DETECTOR.detect(frame)
        if not result:
            continue
        if result.relative_center_x > 0.8 \
           and result.name in flags:
            DRIVER.stop()
            time.sleep(1)
            raise_flag(flag_map[result.name])
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
        result = TASK_DETECTOR.detect(frame)
        if not result:
            continue
        print(result.name)
        if result.name == target \
           and is_valid(result.relative_center_x,
                        result.relative_center_y,
                        target_threshold[result.name]):
            DRIVER.stop()
            time.sleep(1)
            shot_target(2)
            break


def _take_barracks():
    # take_barracks()
    print('take barracks...')


def _capture_target():
    print('capture target...')
    change_camera_direction(2, 'left')
    time.sleep(1)
    # capture_target(1, 2)
    change_camera_direction(2, 'right')


def _transport_forage():
    print('transport forage...')
    # transport_forage(1)
    change_camera_direction(2, 'left')


def _end():
    print('end...')
    global IS_FIRST_FLAGE
    global STATE
    DRIVER.driver_run(20, 20)
    time.sleep(0.5)

    start = time.time()
    while True:
        if time.time() - start > 3:
            break

    DRIVER.stop()
    time.sleep(1)

    IS_FIRST_FLAGE = True
    STATE = 2


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


def wait_start():
    global STATE
    init()
    print('loading finished...')
    buzzing()
    while not START_BUTTON.clicked():  # wait for starting
        pass
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
        result = SIGN_DETECTOR.detect(frame)
        if not result:
            STATE = 0
            TASK_ID = 0
            continue
        STATE = 1
        TASK_ID = result.index
        break


def run():
    state_map = [cruise_processor, task_processor, wait_start]
    while True:
        state_map[STATE]()


if __name__=='__main__':
    run()
