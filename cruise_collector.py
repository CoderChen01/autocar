import os
import time
from datetime import datetime
import multiprocessing

import cv2

import configs
from cart import Cart
from joystick import JoyStick
from logger import Logger
from widgets import Buzzer



class Collector:
    def __init__(self):
        self.js = JoyStick()
        self.js.open()
        self.is_start = multiprocessing.Value('i', 0)
        self.is_restart = multiprocessing.Value('i', 0)
        self.stopped = multiprocessing.Value('i', 0)
        self.is_save = multiprocessing.Value('i', 1)
        self.is_not_save = multiprocessing.Value('i', 1)
        self.x_axis = multiprocessing.Value('d', 0.0)

    def _controller(self):
        while not self.stopped.value:
            _, value, type_, number = self.js.read()
            if self.js.type(type_) == 'button':
                print('button:{} state: {}'.format(number, value))
                if number == 6 and value == 1:  # start
                    self.is_start.value = 1
                    self.is_restart.value = 1
                elif number == 7 and value == 1:  # stop
                    self.is_start.value = 1
                    self.is_restart.value = 0
                    self.stopped.value = 1
                elif number == 1 and value == 1:  # restart
                    self.is_restart.value = 1
                    self.is_start.value = 0
                elif number == 3 and value == 1: # save
                    self.is_save.value = 1
                    self.is_not_save.value = 0
                elif number == 4 and value == 1: # don't save
                    self.is_not_save.value = 1
                    self.is_save.value = 0
            elif self.js.type(type_) == 'axis':
                print('axis:{} state: {}'.format(number, value))
                if number == 2:
                    self.x_axis.value = value / 65534  # -0.5-0.5
                elif number == 0:
                    self.x_axis.value = value / 46810  # -0.7-0.7

    def run(self):
        t = multiprocessing.Process(target=self._controller)
        t.start()
        counter = 0
        sum_circle = 0
        buzzer = Buzzer()
        while True:
            while not self.is_start.value:
                pass
            if not self.is_restart.value:
                break
            _logger = Logger(configs.COLLECTION_SPEED)
            _logger.counter = counter
            _logger.start()
            while self.is_start.value and self.is_restart.value:
                print(self.x_axis.value)
                _logger.log(self.x_axis.value)
            _logger.stop()
            # wait to save
            while True:
                if self.is_save.value and not self.is_not_save.value:
                    sum_circle += 1
                    if sum_circle >= configs.SUM_CIRCLE:
                        for _ in range(3):
                            buzzer.rings()
                            time.sleep(1)
                    counter = _logger.counter
                    break
                if self.is_not_save.value and not self.is_save.value:
                    _logger.remove()
                    buzzer.rings()
                    break
            self.is_save.value = 1
            self.is_not_save.value = 1


if __name__ == "__main__":
    collector = Collector()
    collector.run()
