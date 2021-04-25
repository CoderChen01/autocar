import os
import time
from datetime import datetime
import threading
import json

import cv2

import config
from cart import Cart
from joystick import JoyStick
from camera import Camera


class Logger:
    def __init__(self):
        self.camera = Camera(config.front_cam)
        self.camera.start()
        self.started = False
        self.stopped_ = False
        self.counter = 0
        self.map = {}
        self.result_dir = 'data/' + datetime.now().strftime('%Y%m%d%H%M%S')
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
        self.cart = Cart()
        self.cart.velocity = 35

    def start(self):
        self.started = True
        self.cart.steer(0)

    def stop(self):
        if self.stopped():
            return
        self.stopped_ = True
        self.cart.stop()
        self.camera.stop()
        path = "{}/result.json".format(self.result_dir)
        with open(path, 'w') as fp:
            json.dump(self.map.copy(), fp)

    def log(self, axis):
        if self.started:
            print("axis:".format(axis))
            self.cart.steer(axis)
            image = self.camera.read()
            path = "{}/{}.jpg".format(self.result_dir, self.counter)
            self.map[self.counter] = axis
            cv2.imwrite(path, image)
            self.counter = self.counter + 1

    def stopped(self):
        return self.stopped_


class Collector:
    def __init__(self):
        self.js = JoyStick()
        self.js.open()
        self.logger = Logger()
        self.x_axis = 0


    def _controller(self):
        while not self.logger.stopped():
            _, value, type_, number = self.js.read()
            if self.js.type(type_) == 'button':
                print('button:{} state: {}'.format(number, value))
                if number == 6 and value == 1:
                    self.logger.start()
                if number == 7 and value == 1:
                    self.logger.stop()
            if self.js.type(type_) == 'axis':
                print('axis:{} state: {}'.format(number, value))
                if number == 2:
                    self.x_axis = value * 1.0 / 32767


    def run(self):
        t = threading.Thread(target=self._controller)
        t.start()
        while not self.logger.stopped():
            self.logger.log(self.x_axis)
        t.join()


if __name__ == "__main__":
    collector = Collector()
    collector.run()
