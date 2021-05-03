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
from camera import Camera
from cruiser import Cruiser
from driver import Driver
from cart import Cart


front_camera = Camera(config.front_cam)
side_camera = Camera(config.side_cam)
driver = Driver()
cruiser = Cruiser()
sign_detector = SignDetector()
task_detector = TaskDetector()
start_button = Button(1, 'UP')
stop_button = Button(1, 'DOWN')


def check_stop():
    return stop_button.clicked()

def check_start():
    return start_button.clicked()


if __name__ == '__main__':
    front_camera.start()
    # 基准速度
    driver.set_speed(35)
    # 转弯系数
    driver.cart.Kx = 0.8
    # 延时
    time.sleep(0.5)
    while True:
        if start_button.clicked():
            time.sleep(0.3)
            break
        print("Wait for start!")
    while True:
        front_image = front_camera.read()
        results, low_index = sign_detector.detect(front_image)
        if results:
            pass
        driver.go(front_image)
        if check_stop():
            print("End of program!")
            break
    driver.stop()
    side_camera.stop()
    front_camera.stop()