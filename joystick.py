import struct
import os, struct, array


class JoyStick:
    def __init__(self):
        print('avaliable devices')
        for fn in os.listdir('/dev/input'):
            if fn.startswith('js'):
                print('/dev/input/%s' % fn)

        self.fn = '/dev/input/js0'
        self.jsdev = None
        self.evbuf = None
    
    def open(self):
        self.jsdev = open(self.fn, 'rb')

    def read(self):
        self.evbuf = self.jsdev.read(8)
        return struct.unpack('IhBB', self.evbuf)

    @staticmethod
    def type(type_):
        if type_ & 0x01:
            return 'button'
        if type_ & 0x02:
            return 'axis'

    def get_x_axis(self):
        _, value, type_, number = struct.unpack('IhBB', self.evbuf)
        if number == 1:
            fvalue = value / 32767
            return fvalue


if __name__ == '__main__':
    j = JoyStick()
    j.open()
    while True:
        print(j.read())