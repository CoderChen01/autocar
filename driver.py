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

    def set_speed(self, speed):
        self.cart.velocity = speed

    def driver_run(self, left, right, interval=1, is_stop=True):
        self.cart.move([left, right, left, right])
        if is_stop:
            time.sleep(interval)
            self.stop()

    def go(self, frame, predictor_id=0):
        angle = self.cruiser.cruise(frame, predictor_id)
        self.cart.steer(angle)

    def stop(self):
        self.cart.stop()
        time.sleep(0.5)

    def turn_right_cm(self, distance):
        basespeed = 15
        speed_ratio = 0.4
        drivetime = distance * 0.9
        if distance < 2:
            speed_ratio = 0.2
            drivetime = distance * 0.95
        elif distance < 4:
            speed_ratio = 0.15
            drivetime = distance * 0.75
        else:
            speed_ratio = -0.05
            drivetime = distance * 0.5
        l_speed = basespeed
        r_speed = basespeed * speed_ratio
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(drivetime)
        l_speed = basespeed * speed_ratio
        r_speed = basespeed
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(drivetime)
        self.stop()

    def turn_left_cm(self, distance):
        basespeed = 15
        speed_ratio = 0.4
        drivetime = distance * 0.9
        if distance < 2:
            speed_ratio = 0.2
            drivetime = distance * 0.95
        elif distance < 4:
            speed_ratio = 0.15
            drivetime = distance * 0.75
        else:
            speed_ratio = -0.05
            drivetime = distance * 0.5
        l_speed = basespeed * speed_ratio
        r_speed = basespeed
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(drivetime)
        l_speed = basespeed
        r_speed = basespeed * speed_ratio
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(drivetime)
        self.stop()


if __name__ == '__main__':
    time.sleep(5)
    driver = Driver()
    driver.turn_left_cm(0.5)
