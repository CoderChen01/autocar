import time
import math
from ctypes import *

from serial_port import _serial as serial

comma_head_01_motor = bytes.fromhex('77 68 06 00 02 0C 01 01')  # front-left
comma_head_02_motor = bytes.fromhex('77 68 06 00 02 0C 01 02')  # front-right -
comma_head_03_motor = bytes.fromhex('77 68 06 00 02 0C 01 03')  # rear-left
comma_head_04_motor = bytes.fromhex('77 68 06 00 02 0C 01 04')  # rear-right -
comma_trail = bytes.fromhex('0A')

class Cart:
    def __init__(self):
        self.velocity = 25
        self.serial = serial

    def steer(self, angle):
        turn_speed = int(self.velocity)
        leftwheel = int(self.velocity)
        rightwheel = int(self.velocity)
        if abs(angle) > 0.4:
            turn_speed = int(self.velocity * 0.92)
        elif 0.015 < abs(angle) < 0.05:
            turn_speed = int(self.velocity * 0.8)
        if angle < 0:
            leftwheel = int((1 + angle) * turn_speed)
        elif angle > 0:
            rightwheel = int((1 - angle) * turn_speed)
        self.move([leftwheel, rightwheel, leftwheel, rightwheel])

    def stop(self):
        self.move([0, 0, 0, 0])

    @staticmethod
    def exchange(speed):
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100
        else:
            speed = speed
        return speed

    def move(self, speeds):
        left_front = int(speeds[0])
        right_front = -int(speeds[1])
        left_rear = int(speeds[2])
        right_rear = -int(speeds[3])
        left_front=self.exchange(left_front)
        right_front = self.exchange(right_front)
        left_rear=self.exchange(left_rear)
        right_rear = self.exchange(right_rear)
        send_data_01_motor = comma_head_01_motor \
                             + left_front.to_bytes(1, byteorder='big', signed=True) \
                             + comma_trail
        send_data_02_motor = comma_head_02_motor \
                             + right_front.to_bytes(1, byteorder='big', signed=True) \
                             + comma_trail
        send_data_03_motor = comma_head_03_motor \
                             + left_rear.to_bytes(1, byteorder='big', signed=True) \
                             + comma_trail
        send_data_04_motor = comma_head_04_motor \
                             + right_rear.to_bytes(1, byteorder='big', signed=True) \
                             + comma_trail

        self.serial.write_raw(send_data_01_motor)
        self.serial.write_raw(send_data_02_motor)
        self.serial.write_raw(send_data_03_motor)
        self.serial.write_raw(send_data_04_motor)

    def turn_left(self):
        speed = self.velocity 
        leftwheel = speed
        rightwheel = -speed
        self.move([leftwheel, rightwheel, leftwheel, rightwheel])

    def turn_right(self):
        speed = self.velocity 
        leftwheel = -speed
        rightwheel = speed
        self.move([leftwheel, rightwheel, leftwheel, rightwheel])
        print("L:{} R:{}".format(leftwheel, rightwheel))

    def reverse(self):
        speed = self.velocity 
        self.move([-speed,-speed,-speed,-speed])
