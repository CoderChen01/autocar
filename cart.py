import time
import math
from ctypes import *

from serial_port import _serial as serial
from simple_pid import PID

comma_head_01_motor = bytes.fromhex('77 68 06 00 02 0C 01 01')  # front-left
comma_head_02_motor = bytes.fromhex('77 68 06 00 02 0C 01 02')  # front-right -
comma_head_03_motor = bytes.fromhex('77 68 06 00 02 0C 01 03')  # rear-left
comma_head_04_motor = bytes.fromhex('77 68 06 00 02 0C 01 04')  # rear-right -
comma_trail = bytes.fromhex('0A')

class Cart:
    def __init__(self):
        self.velocity = 25
        self.serial = serial
        self.i = 0
        self.p = 0
        self.d = 0

    def _coefficient(self, angle):
        kp = 0.9
        ki = 0.005
        kd = 0.6
        p = kp * angle
        i = ki * self.i
        d = kd * (angle - self.d)
        coefficient = p + i + d
        self.d = angle
        self.i += angle
        if coefficient > 1:
            coefficient = 1
        if self.i > 1:
            self.i = 1
        print(f'angle: {angle}, p: {p}, i: {i}, d: {d}, coefficient: {coefficient}')
        return coefficient


    def steer(self, angle):
        turn_speed = int(self.velocity)
        leftwheel = int(self.velocity)
        rightwheel = int(self.velocity)
        coefficient = self._coefficient(angle)
        abs_coefficient = abs(coefficient)
        if 0.0001 < abs_coefficient < 0.1:
            turn_speed = turn_speed * (1 - abs_coefficient) * 0.92
        # elif 0.1 <= abs_angle < 0.2:
        #     turn_speed = turn_speed * (1 - coefficient * 0.8)
        else:
            turn_speed = turn_speed * (1 - abs_coefficient)
        if angle < 0:
            leftwheel = turn_speed
        elif angle > 0:
            rightwheel = turn_speed
        print(turn_speed)
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
