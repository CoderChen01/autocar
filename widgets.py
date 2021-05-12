import threading
import time
import struct

import cv2
import serial

import config
from serial_port import Serial


class Serial0:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0',
                                115200,
                                timeout=1,
                                parity=serial.PARITY_NONE,
                                stopbits=1)
    def __del__(self):
        self.serial.close()


class Serial1:
    def __init__(self):
        self.serial = Serial()

    def __del__(self):
        self.serial.close()


class Light(Serial0):
    def __init__(self, port):
        super(Light, self).__init__()
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
        self.serial.write(cmd_servo_data)

    @staticmethod
    def lightoff():
        cmd_servo_data1 = bytes.fromhex('77 68 08 00 02 3B 02 00 00 00 00 0A')
        cmd_servo_data2 = bytes.fromhex('77 68 08 00 02 3B 03 00 00 00 00 0A')
        cmd_servo_data = cmd_servo_data1 + cmd_servo_data2
        self.serial.write(cmd_servo_data)


class UltrasonicSensor(Serial1):
    def __init__(self, port):
        super(UltrasonicSensor, self).__init__()
        self.port = port
        port_str = '{:02x}'.format(port)
        self.cmd_data = bytes.fromhex('77 68 04 00 01 D1 {} 0A'.format(port_str))

    def read(self):
        self.serial.write(self.cmd_data)
        return_data = self.serial.read()
        if len(return_data) < 11 \
                or return_data[7] != 0xD1 \
                or return_data[8] != self.port:
            return None
        return_data_ultrasonic = return_data[3:7]
        ultrasonic_sensor = struct.unpack('<f', struct.pack('4B', *return_data_ultrasonic))[0]
        return int(ultrasonic_sensor)


class Buzzer(Serial0):
    def __init__(self):
        super(Buzzer, self).__init__()
        self.cmd_data = bytes.fromhex('77 68 06 00 02 3D 03 02 0A')
        self.serial = serial.Serial('/dev/ttyUSB0',
                                115200,
                                timeout=1,
                                parity=serial.PARITY_NONE,
                                stopbits=1)

    def rings(self):
        self.serial.write(self.cmd_data)


class Button(Serial1):
    def __init__(self, port, buttonstr):
        super(Button, self).__init__()
        self.state = False
        self.port = port
        self.buttonstr = buttonstr
        port_str = '{:02x}'.format(port)
        self.cmd_data = bytes.fromhex('77 68 05 00 01 E1 {} 01 0A'.format(port_str))
        self.serial = Serial()

    def clicked(self):
        self.serial.write(self.cmd_data)
        response = self.serial.read()
        buttonclick = 'no'
        if len(response) == 9 and response[5] == 0xE1 and response[6] == self.port:
            button_byte = response[3:5] + bytes.fromhex('00 00')
            button_value = struct.unpack('<i', struct.pack('4B', *button_byte))[0]
            # print("%x"%button_value)
            if 0x1f1 <= button_value <= 0x20f:
                buttonclick = 'UP'
            elif 0x330 <= button_value <= 0x33f:
                buttonclick = 'LEFT'
            elif 0x2ff <= button_value <= 0x30f:
                buttonclick = 'DOWN'
            elif 0x2a0 <= button_value <= 0x2af:
                buttonclick = 'RIGHT'
        return self.buttonstr == buttonclick


class MotorRotate(Serial0):
    def __init__(self, port):
        super(MotorRotate, self).__init__()
        self.port = port
        self.port_str = '{:02x}'.format(port)
        self.serial = serial.Serial('/dev/ttyUSB0',
                                115200,
                                timeout=1,
                                parity=serial.PARITY_NONE,
                                stopbits=1)

    def motor_rotate(self, speed):
        cmd_servo_data = bytes.fromhex('77 68 06 00 02 0C 02') \
                         + bytes.fromhex(self.port_str) \
                         + speed.to_bytes(1, byteorder='big', signed=True) \
                         + bytes.fromhex('0A')
        self.serial.write(cmd_servo_data)


class ServoPWM(Serial0):
    def __init__(self, ID):
        super(ServoPWM, self).__init__()
        self.ID = ID
        self.ID_str = '{:02x}'.format(ID)
        self.serial = serial.Serial('/dev/ttyUSB0',
                                115200,
                                timeout=1,
                                parity=serial.PARITY_NONE,
                                stopbits=1)

    def servocontrol(self, angle, speed):
        cmd_servo_data = bytes.fromhex('77 68 06 00 02 0B') \
                         + bytes.fromhex(self.ID_str) \
                         + speed.to_bytes(1, byteorder='big', signed=True) \
                         + angle.to_bytes(1, byteorder='big', signed=False) \
                         + bytes.fromhex('0A')
        self.serial.write(cmd_servo_data)


class Servo(Serial0):
    def __init__(self, ID):
        super(Servo, self).__init__()
        self.ID = ID
        self.ID_str = '{:02x}'.format(ID)
        self.serial = serial.Serial('/dev/ttyUSB0',
                                115200,
                                timeout=1,
                                parity=serial.PARITY_NONE,
                                stopbits=1)

    def servocontrol(self, angle, speed):
        cmd_servo_data = bytes.fromhex('77 68 06 00 02 36') \
                         + bytes.fromhex(self.ID_str) \
                         + speed.to_bytes(1, byteorder='big',signed=True) \
                         + angle.to_bytes(1, byteorder='big', signed=True) \
                         + bytes.fromhex('0A')
        self.serial.write(cmd_servo_data)
