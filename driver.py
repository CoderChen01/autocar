import os
import sys
import time

from cruiser import Cruiser
from cart import Cart


SLOW_DOWN_RATE = 0.6


class Driver:
    def __init__(self):
        self.max_speed = 25
        self.full_speed = 25
        self.cart = Cart()
        self.cart.velocity = self.full_speed
        self.cruiser = Cruiser()

    def driver_run(self, left, right):
        self.cart.move([left, right, left, right])

    def go(self, frame):
        angle = self.cruiser.cruise(frame)
        self.cart.steer(angle)

    def stop(self):
        self.cart.stop()

    def turn_right(self, basespeed):
        l_speed = basespeed
        r_speed = basespeed * 0.4
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(1.5)
        l_speed = basespeed * 0.4
        r_speed = basespeed
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(1.3)
        self.cart.stop()

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
        time.sleep(drivetime - 0.5)
        self.cart.stop()

    def turn_left(self, basespeed):
        l_speed = basespeed * 0.4
        r_speed = basespeed
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(1.5)
        l_speed = basespeed
        r_speed = basespeed * 0.4
        self.cart.move([l_speed, r_speed, l_speed, r_speed])
        time.sleep(1.3)
        self.cart.stop()
        time.sleep(0.3)

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
        time.sleep(drivetime - 0.5)
        self.cart.stop()
        time.sleep(0.3)
