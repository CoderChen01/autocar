import threading
import time
import struct

import cv2

from serial_port import _serial as serial


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
        serial.write_raw(cmd_servo_data)

    @staticmethod
    def lightoff():
        cmd_servo_data1 = bytes.fromhex('77 68 08 00 02 3B 02 00 00 00 00 0A')
        cmd_servo_data2 = bytes.fromhex('77 68 08 00 02 3B 03 00 00 00 00 0A')
        cmd_servo_data = cmd_servo_data1 + cmd_servo_data2
        serial.write_raw(cmd_servo_data)


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


class Buzzer:
    def __init__(self):
        self.cmd_data = bytes.fromhex('77 68 06 00 02 3D 03 02 0A')

    def rings(self):
        serial.write_raw(self.cmd_data)


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
        buttonclick = 'no'
        if len(response) == 9 and response[5] == 0xE1 and response[6] == self.port:
            button_byte = response[3:5] + bytes.fromhex('00 00')
            button_value = struct.unpack('<i', struct.pack('4B', *button_byte))[0]
            if 0x1f1 <= button_value <= 0x20f:
                buttonclick = 'UP'
            elif 0x157 <= button_value <= 0x160:
                buttonclick = 'LEFT'
            elif 0x2ff <= button_value <= 0x30f:
                buttonclick = 'DOWN'
            elif 0x57 <= button_value <= 0x5a:
                buttonclick = 'RIGHT'
        return self.buttonstr == buttonclick


class MotorRotate:
    def __init__(self, port):
        self.port = port
        self.port_str = '{:02x}'.format(port)

    def motor_rotate(self, speed):
        cmd_servo_data = bytes.fromhex('77 68 06 00 02 0C 02') \
                         + bytes.fromhex(self.port_str) \
                         + speed.to_bytes(1, byteorder='big', signed=True) \
                         + bytes.fromhex('0A')
        serial.write_raw(cmd_servo_data)


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
        serial.write_raw(cmd_servo_data)


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
        serial.write_raw(cmd_servo_data)


if __name__ == '__main__':
    # b = Button(1, 'LEFT')
    # while True:
    #     print(b.clicked())
    s = ServoPWM(6)
    s.servocontrol(0, 100)
    time.sleep(2)
    s.servocontrol(200, 100)
    time.sleep(2)