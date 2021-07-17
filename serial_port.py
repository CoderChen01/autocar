import time
from threading import Lock

import serial


class Serial:
    def __init__(self):
        portxs = [f"/dev/ttyUSB{i}" for i in range(3)]
        bps = 115200
        for portx in portxs:
            try:
                self.serial = serial.Serial(portx,
                                            bps,
                                            timeout=1,
                                            parity=serial.PARITY_NONE,
                                            stopbits=1)
                time.sleep(1)
                self.serial.write(bytes.fromhex('77 68 02 00 01 0A'))
                res = self.serial.readline()
                if res == b'\x00\x00\r\n':
                    self.portx = portx
                    break
            except Exception as e:
                continue
        self.res = None

    def write(self, data):
        lock = Lock()
        lock.acquire()
        try:
            self.serial.write(data)
            self.serial.flush()
            self.res = self.serial.readline()
        finally:
            lock.release()

    def read(self):
        return self.res

    def write_raw(self, data):
        self.serial.write(data)
        
    def close(self):
        self.serial.close()


_serial = Serial()
