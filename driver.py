import os
import sys
import time

import configs
from cruiser import Cruiser
from cart import Cart


class Driver:
    def __init__(self):
        self.cart = Cart()
        self.cart.velocity = configs.LOW_RUN_SPEED
        self.cruiser = Cruiser()

    def set_speed(self, speed):
        self.cart.velocity = speed

    def get_speed(self):
        return self.cart.velocity

    def driver_run(self, left, right, interval=1, is_stop=True):
        self.cart.move([left, right, left, right])
        if is_stop:
            time.sleep(interval)
            self.cart.stop()
            time.sleep(0.5)

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

    def stop(self):
        self.cart.stop()
        time.sleep(0.5)
        if self.get_speed() >= 50:
            self.driver_run(-10, -10, 0.66)
