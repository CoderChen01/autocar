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


class Runner:
    def __init__(self):
        self.is_run = mp.Value('i', 0)
        self.state = mp.Value('i', 0)
        self.task_id = mp.Value('i', 0)
        self.side_camera_direction = mp.Value('i', 0)

    def task_processor(self):
        task_detector = TaskDetector()
        side_camera = Camera(config.side_cam)
        side_camera.start()
        while self.is_run.value:
            if not self.state.value:  # Wait for cruising
                continue
            # TODO

        side_camera.stop()

    def cruise_processor(self):
        cruiser = Cruiser()
        driver = Driver()
        sign_detector = SignDetector()
        front_camera = Camera(config.front_cam)
        front_camera.start()
        while self.is_run.value:
            if self.state.value:  # Wait for a task
                continue
            # TODO
            frame = front_camera.read()
            sign_result = sign_detector.detect(frame)
            if self.has_sign(sign_result):  # change state to task
                self.change_state(True)
                continue
            angle = cruiser.cruise(frame)  # get angle from frame
            driver.go(angle)
        front_camera.stop()
    
    def run(self):
        start_button = Button(1, 'UP')
        stop_button = Button(1, 'DOWN')
        cruise_processor = mp.Process(target=self.cruise_processor)
        task_processor = mp.Process(target=self.task_processor)
        while not start_button.clicked():  # wait for starting
            pass
        self.is_run.value = 1  # change running state
        cruise_processor.start()  # start cruise processor
        task_processor.start()  # start task processor
        while not stop_button.clicked():  # wait for stopping
            pass
        self.is_run.value = 0  # change running state

    @staticmethod
    def has_sign(sign_result):
        """
        determine if the task is approaching
        """
        nearest = sign_result[0][sign_result[1]]
        if nearest.relative_center_y > config.HAS_SIGN_THRESHOLD:
            return True
        return False

    def dispatch_task(self, sign_result):
        """
        set tasks based on the detection
        """
        nearest = sign_result[0][sign_result[1]]
        task_id = nearest.index
        if task_id:
            self.task_id.value = task_id

    def change_state(self, is_task):
        if is_task:
            self.state.value = 1
        else:
            self.state.value = 0


if __name__ == '__main__':
    # TODO 我打算先使用串行方式编码调试效果，
    #  模型返回结果为detectors.DetectionResult类
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