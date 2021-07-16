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

    def _coefficient(self, angle):
        abs_angle = abs(angle)
        if abs_angle <= 0.0005:
            coefficient = 1
        elif 0.0005 < abs_angle < 0.001:
            coefficient = (1 - abs_angle) * 0.93
        elif 0.001 <= abs_angle < 0.01:
            coefficient = (1 - abs_angle) * 0.96
        elif 0.01 <= abs_angle < 0.1:
            coefficient = (1 - abs_angle) * 0.97
        else:
            coefficient = 0.8 * math.exp(-1.5 * abs_angle)
        print(f'{abs_angle},{coefficient}')
        return coefficient

    def steer(self, angle):
        turn_speed = int(self.velocity)
        leftwheel = int(self.velocity)
        rightwheel = int(self.velocity)
        coefficient = self._coefficient(angle)
        if angle < 0:
            leftwheel = turn_speed * coefficient
        elif angle > 0:
            rightwheel = turn_speed * coefficient
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
