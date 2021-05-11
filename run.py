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
    def __init__(self, speed=35):
        self.speed = speed
        self.is_run = mp.Value('i', 0)
        self.state = mp.Value('i', 0)
        self.task_id = mp.Value('i', 0)
        self.task_param = mp.Array('i', [0, 0])
        self.side_camera_direction = mp.Value('i', 0)

    def task_processor(self):
        driver = Driver()
        task_detector = TaskDetector()
        side_camera = Camera(config.side_cam)
        side_camera.start()
        while self.is_run.value:
            if not self.state.value:  # Wait for cruising
                continue
            results = task_detector.detect(side_camera.read())
            if self.task_id.value == 3:  # raise flag
                if results[0].index == 1:
                    raise_flag(3)
                elif results[0].index == 2:
                    raise_flag(4)
                elif results[0].index == 3:
                    raise_flag(5)
            elif self.task_id.value == 5:
                shot_target(2)
            elif self.task_id.value == 1:
                take_barracks()
            elif self.task_id.value == 2:
                capture_target(2, 2)
            elif self.task_id.value == 4:
                transport_forage(1)
        side_camera.stop()

    def cruise_processor(self):
        cruiser = Cruiser()
        driver = Driver()
        sign_detector = SignDetector()
        front_camera = Camera(config.front_cam)
        front_camera.start()
        has_sign = False
        first_result = None
        while self.is_run.value:
            if self.state.value:  # Wait for a task
                continue
            frame = front_camera.read()
            sign_result = sign_detector.detect(frame)
            if not has_sign and self.has_sign(sign_result):
                has_sign = True
                first_result = sign_result
            if has_sign and not has_sign(sign_result):
                driver.stop()
                self.dispatch_task(first_result)
                self.change_state(True)
                has_sign = False
                first_result = None
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
        if sign_result[1] == -1:
            return False
        return True

    def dispatch_task(self, sign_result):
        """
        set tasks based on the detection
        """
        nearest = sign_result[0][sign_result[1]]  # results[blow_center_index]
        task_id = nearest.index
        if task_id:
            self.task_id.value = task_id

    def change_state(self, is_task):
        if is_task:
            self.state.value = 1
        else:
            self.state.value = 0


if __name__ == '__main__':
    runner = Runner()
    runner.run()
