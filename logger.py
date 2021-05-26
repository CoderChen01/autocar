import os
import time
import threading
from datetime import datetime
import json

import cv2

import configs
from cart import Cart
from improved_videocapture import BackgroundVideoCapture


class Logger:
    def __init__(self, velocity=20):
        self.camera = cv2.VideoCapture(configs.FRONT_CAM)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.started = False
        self.stopped_ = False
        self.counter = 0
        self.map = {}
        self.result_dir = 'data/' + datetime.now().strftime('%Y%m%d%H%M%S')
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
        self.cart = Cart()
        self.cart.velocity = velocity

    def start(self):
        self.started = True
        self.cart.steer(0)

    def stop(self):
        if self.stopped():
            return
        self.stopped_ = True
        self.cart.stop()
        self.camera.release()
        path = "{}/result.json".format(self.result_dir)
        with open(path, 'w') as fp:
            json.dump(self.map.copy(), fp)

    def log(self, axis):
        if self.started:
            self.cart.steer(axis)
            _, image = self.camera.read()
            path = "{}/{}.jpg".format(self.result_dir, self.counter)
            self.map[self.counter] = axis
            cv2.imwrite(path, image)
            self.counter = self.counter + 1
            time.sleep(0.08)

    def stopped(self):
        return self.stopped_
