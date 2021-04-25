import threading
import time
import struct

import cv2

import config
from serial_port import serial_connection


serial = serial_connection


class Light:
    def __init__(self, port):
        self.port = port
        self.port_str = '{:02x}'.format(port)

    def lightcontrol(self, which, Red, Green, Blue):
        which_str = '{:02x}'.format(which)
        Red_str = '{:02x}'.format(Red)
        Green_str = '{:02x}'.format(Green)
        Blue_str = '{:02x}'.format(Blue)
        cmd_servo_data = bytes.fromhex(
            '77 68 08 00 02 3B {} {} {} {} {} 0A'
                .format(self.port_str, which_str, Red_str, Green_str, Blue_str))
        serial.write(cmd_servo_data)

    @staticmethod
    def lightoff():
        cmd_servo_data1 = bytes.fromhex('77 68 08 00 02 3B 02 00 00 00 00 0A')
        cmd_servo_data2 = bytes.fromhex('77 68 08 00 02 3B 03 00 00 00 00 0A')
        cmd_servo_data = cmd_servo_data1 + cmd_servo_data2
        serial.write(cmd_servo_data)


class UltrasonicSensor:
    def __init__(self, port):
        self.port = port
        port_str = '{:02x}'.format(port)
        self.cmd_data = bytes.fromhex('77 68 04 00 01 D1 {} 0A'.format(port_str))

    def read(self):
        serial.write(self.cmd_data)
        return_data = serial.read()
        if len(return_data) < 11 \
                or return_data[7] != 0xD1 \
                or return_data[8] != self.port:
            return None
        return_data_ultrasonic = return_data[3:7]
        ultrasonic_sensor = struct.unpack('<f', struct.pack('4B', *return_data_ultrasonic))[0]
        return int(ultrasonic_sensor)


class MagnetoSensor:
    def __init__(self, port):
        self.port = port
        port_str = '{:02x}'.format(self.port)
        self.cmd_data = bytes.fromhex('77 68 04 00 01 CF {} 0A'.format(port_str))

    def read(self):
        serial.write(self.cmd_data)
        return_data = serial.read()
        # print("return_data=",return_data[8])
        if len(return_data) < 11 \
                or return_data[7] != 0xCF \
                or return_data[8] != self.port:
            return None
        # print(return_data.hex())
        return_data = return_data[3:7]
        mag_sensor = struct.unpack('<i', struct.pack('4B', *return_data))[0]
        # print(ultrasonic_sensor)
        return int(mag_sensor)


class Buzzer:
    def __init__(self):
        self.cmd_data = bytes.fromhex('77 68 06 00 02 3D 03 02 0A')

    def rings(self):
        serial.write(self.cmd_data)


class Button:
    def __init__(self, port, buttonstr):
        self.state = False
        self.port = port
        self.buttonstr = buttonstr
        port_str = '{:02x}'.format(port)
        self.cmd_data = bytes.fromhex('77 68 05 00 01 E1 {} 01 0A'.format(port_str))

    def clicked(self):
        serial.write(self.cmd_data)
        response = serial.read()
        buttonclick="no"
        if len(response) == 9 and  response[5] == 0xE1 and response[6] == self.port:
            button_byte=response[3:5]+bytes.fromhex('00 00')
            button_value=struct.unpack('<i', struct.pack('4B', *button_byte))[0]
            # print("%x"%button_value)
            if 0x1f1 <= button_value <= 0x20f:
                buttonclick="UP"
            elif 0x330 <= button_value <= 0x33f:
                buttonclick = "LEFT"
            elif 0x2ff <= button_value <= 0x30f:
                buttonclick = "DOWN"
            elif 0x2a0 <= button_value <= 0x2af:
                buttonclick = "RIGHT"
        return self.buttonstr==buttonclick


class MotorRotate:
    def __init__(self, port):
        self.port = port
        self.port_str = '{:02x}'.format(port)

    def motor_rotate(self, speed):
        cmd_servo_data = bytes.fromhex('77 68 06 00 02 0C 02') \
                         + bytes.fromhex(self.port_str) \
                         + speed.to_bytes(1, byteorder='big', signed=True) \
                         + bytes.fromhex('0A')
        serial.write(cmd_servo_data)


class ServoPWM:
    def __init__(self, ID):
        self.ID = ID
        self.ID_str = '{:02x}'.format(ID)

    def servocontrol(self, angle, speed):
        cmd_servo_data = bytes.fromhex('77 68 06 00 02 0B') \
                         + bytes.fromhex(self.ID_str) \
                         + speed.to_bytes(1, byteorder='big', signed=True) \
                         + angle.to_bytes(1, byteorder='big', signed=False) \
                         + bytes.fromhex('0A')
        serial.write(cmd_servo_data)


class Servo:
    def __init__(self, ID):
        self.ID = ID
        self.ID_str = '{:02x}'.format(ID)

    def servocontrol(self, angle, speed):
        cmd_servo_data = bytes.fromhex('77 68 06 00 02 36') \
                         + bytes.fromhex(self.ID_str) \
                         + speed.to_bytes(1, byteorder='big',signed=True) \
                         + angle.to_bytes(1, byteorder='big', signed=True) \
                         + bytes.fromhex('0A')
        serial.write(cmd_servo_data)


class LimitSwitch:
    def __init__(self, port):
        self.state = False
        self.port = port
        self.state = True
        port_str = '{:02x}'.format(port)
        # print (port_str)
        self.cmd_data = bytes.fromhex('77 68 04 00 01 DD {} 0A'.format(port_str))

    # print('77 68 04 00 01 DD {} 0A'.format(port_str))

    def clicked(self):
        serial.write(self.cmd_data)
        response = serial.read()  # 77 68 01 00 0D 0A
        if len(response) < 8 or response[4] != 0xDD or response[5] != self.port \
                or response[2] != 0x01:
            return False
        state = response[3] == 0x01
        # print("state=",state)
        # print("elf.state=", self.state)
        clicked = False
        if state == True and self.state == True and clicked == False:
            clicked = True
        if state == False and self.state == True and clicked == True:
            clicked = False
        # print('clicked=',clicked)
        return clicked


class InfraredValue:
    def __init__(self, port):
        port_str = '{:02x}'.format(port)
        self.cmd_data = bytes.fromhex('77 68 04 00 01 D1 {} 0A'.format(port_str))

    def read(self):
        serial.write(self.cmd_data)
        return_data = serial.read()
        if return_data[2] != 0x04:
            return None
        if return_data[3] == 0x0a:
            return None
        # print("**********************************")
        # print("return_data[3]=%x" % return_data[3])
        # print(type(return_data[3]))
        # print("return_data[4]=%x" % return_data[4])
        # print("return_data[5]=%x" % return_data[5])
        # print("return_data[6]=%x" % return_data[6])
        # print(return_data.hex())
        return_data_infrared = return_data[3:7]
        print(return_data_infrared)
        infrared_sensor = struct.unpack('<i', struct.pack('4B', *return_data_infrared))[0]
        # print(ultrasonic_sensor)
        return infrared_sensor


if __name__ == '__main__':
    # m = MotorRotate(1)
    m2 = MotorRotate(2)
    # m3 = MotorRotate(3)
    # m4 = MotorRotate(4)
    # m.motor_rotate(30)
    m2.motor_rotate(-40)
    # m3.motor_rotate(30)
    # m4.motor_rotate(-30)
    time.sleep(30)