import os
import sys
import time

import configs
from cruiser import Cruiser
from cart import Cart


class Driver:
    def __init__(self):
        self.cart = Cart()
        self.cart.velocity = configs.RUN_SPEED
        self.cruiser = Cruiser()
        self.cart.w1 = 0.88
        self.cart.w2 = 1.88

    def set_w(self, w1, w2):
        self.cart.w1 = w1
        self.cart.w2 = w2

    def set_speed(self, speed):
        self.cart.velocity = speed

    def get_speed(self):
        return self.cart.velocity

    def go(self, frame, weights=None):
        """
        Multimodel fusion
        """
        angle = 0
        if weights is None:
            weights = [0] * self.cruiser.predictors_num
            weights[0] = 1
        for index in range(self.cruiser.predictors_num):
            weight = weights[index]
            if weight != 0:
                angle += weight * self.cruiser.cruise(frame, index)
        self.cart.steer(angle)
        return angle

    def driver_run(self, left, right, interval=1, is_stop=True):
        self.cart.move([left, right, left, right])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def right_run(self, speed, interval=1, is_stop=True):
        self.cart.move([speed, -speed, -speed, speed])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def left_run(self, speed, interval=1, is_stop=True):
        self.cart.move([-speed, speed, speed, -speed])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def left_forward_run(self, speed, interval=1, is_stop=True):
        self.cart.move([0, speed, speed, 0])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def right_forward_run(self, speed, interval=1, is_stop=True):
        self.cart.move([speed, 0, 0, speed])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def left_backward_run(self, speed, interval=1, is_stop=True):
        self.cart.move([-speed, 0, 0, -speed])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def right_backward_run(self, speed, interval=1, is_stop=True):
        self.cart.move([0, -speed, -speed, 0])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def right_circle_run(self, speed, interval=1, is_stop=True):
        self.cart.move([speed, -speed, speed, -speed])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def left_circle_run(self, speed, interval=1, is_stop=True):
        self.cart.move([-speed, speed, -speed, speed])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.066)

    def stop(self):
        if self.get_speed() >= 50:
            self.driver_run(-10, -10, 0.66)
        self.cart.stop()
        time.sleep(0.066)
