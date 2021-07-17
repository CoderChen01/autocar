import re
import time
from threading import Lock

import serial

from serial_port import _serial


class Distance:
    def __init__(self):
        portxs = [f"/dev/ttyUSB{i}" for i in range(3)]
        bps = 115200
        for portx in portxs:
            if portx == _serial.portx:
                continue
            try:
                self.serial = serial.Serial(portx,
                                            bps,
                                            timeout=1,
                                            parity=serial.PARITY_NONE,
                                            stopbits=1)
                time.sleep(1)
                res = self.serial.read(33)
                if len(res) == 33:
                    self.portx = portx
                    break
            except Exception as e:
                continue
        self.last_output = 0

    def get_distance(self):
        state = None
        distance_mm = None
        for _ in range(10):
            raw_data = self.serial.readline().decode('utf8').strip()
            if not raw_data:
                continue
            state_index = raw_data.find('State')
            if raw_data.find('State') != -1:
                state = int(raw_data[6])
            elif raw_data.find('d') != -1:
                distance = re.search('\d+\.?\d*', raw_data)
                if not distance:
                    continue
                else:
                    distance_mm = int(distance.group())
            else:
                continue
            if state is not None \
                and distance_mm is not None:
                break
        return state, distance_mm


if __name__ == "__main__":
    d = Distance()
    while True:
        print(d.get_distance())
