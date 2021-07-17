import time
from threading import Lock

import minimalmodbus

from serial_port import _serial

class Distance:
    def __init__(self):
        portxs = [f'/dev/ttyUSB{i}' for i in range(3)]
        for portx in portxs:
            # if portx == _serial.portx:
            #     continue
            try:
                self.laser = minimalmodbus.Instrument(portx, 0x50)
                self.laser.serial.baudrate = 115200
                distance = self.laser.read_register(0x34, 1)
                if distance:
                    self.portx = portx
                    break
            except Exception as e:
                continue
        self.last_output = 0

    def get_istance(self):
        try:
            distance = self.laser.read_register(0x34, 1)
            self.last_output = distance
            return distance
        except Exception:
            return self.last_output


if __name__ == "__main__":
    Distance()
    # while True:
    #     serial_connection = Distance()
    #     print(serial_connection.get_istance())
