# import threading
#
# from joystick import JoyStick
# from cart import Cart
#
# js = JoyStick()
# def joystick_thread():
#     js.open()
#     while True:
#         type_, code, value = js.read()
#         if js.type(type_) == 'button':
#             if code == 310:
#                 logger.start()
#             if code == 311:
#                 logger.stop()
#         if js.type(type_) == 'axis':
#             print(value)
#             if code == 2:
#                 value = value - 127
#                 js.x_axis = value * 1.0 / 127
#
# if __name__ == '__main__':
#     t = threading.Thread(target=joystick_thread, args=())
#     t.start()
#     c = Cart()
#     while True:
#         c.steer(js.x_axis)
import struct

import config

with open(config.JOYSTICK_ADDR, 'rb') as joystick:
    while True:
        buff = joystick.read(8)
        time, value, type_, number = struct.unpack('IhBB', buff)
        print(time, value, type_, number )