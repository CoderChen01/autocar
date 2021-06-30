import time

import configs
from widgets import *
from driver import Driver


def buzzing(num=3):
    buzzer = Buzzer()
    for _ in range(num):
        buzzer.rings()
        time.sleep(1)


def light_work(light_port, color):
    light = Light(light_port)
    red = [80, 0, 0]
    green = [0, 80, 0]
    yellow = [80, 80, 0]
    off = [0, 0, 0]
    light_color = [0, 0, 0]
    if color == 'red':
        light_color = red
    elif color == 'green':
        light_color = green
    elif color == 'yellow':
        light_color = yellow
    elif color == 'off':
        light_color = off
    light.lightcontrol(0, light_color[0], light_color[1], light_color[2])


def raise_flag(servo_port):
    servo = ServoPWM(servo_port)
    servo.servocontrol(120, 100)
    time.sleep(0.5)
    for _ in range(3):
        light_work(2, 'green')
        time.sleep(2)
        light_work(2, 'off')
        time.sleep(0.5)
    servo.servocontrol(10, 100)
    time.sleep(0.5)


def shot_target(motor_port=2):
    setmotor1 = MotorRotate(motor_port)
    time.sleep(0.5)
    setmotor1.motor_rotate(70)
    time.sleep(0.6)
    setmotor1.motor_rotate(0)
    time.sleep(0.3)
    setmotor1.motor_rotate(-70)
    time.sleep(0.5)
    setmotor1.motor_rotate(0)
    time.sleep(1)


def take_barracks():
    driver = Driver()
    driver.driver_run(5, 20)
    time.sleep(1.5)
    driver.driver_run(10, 10)
    time.sleep(4)
    driver.driver_run(20, 5)
    time.sleep(1.5)
    driver.stop()
    for _ in range(3):
        light_work(2, 'red')
        time.sleep(2)
        light_work(2, 'off')
        time.sleep(0.5)
    driver.driver_run(-10, -10)
    time.sleep(3)
    driver.driver_run(20, 5)
    time.sleep(2)
    driver.driver_run(10, 10)
    time.sleep(2)
    driver.driver_run(5, 20)
    time.sleep(2)


def capture_target(servo_485_id=1, servo_pwm_id=2, motor_port=2):
    servo1 = Servo(servo_485_id)
    servo2 = ServoPWM(servo_pwm_id)
    setmotor1 = MotorRotate(motor_port)
    setmotor1.motor_rotate(70)
    time.sleep(0.6)
    setmotor1.motor_rotate(0)
    time.sleep(0.3)
    servo2.servocontrol(90, 100)
    time.sleep(2)
    servo1.servocontrol(-15, 30)
    time.sleep(3)
    servo2.servocontrol(180, 100)
    time.sleep(2)
    servo1.servocontrol(-80,100)
    time.sleep(3)
    setmotor1.motor_rotate(-70)
    time.sleep(0.5)
    setmotor1.motor_rotate(0)
    time.sleep(1)


def transport_forage(server485_id=2, servopwm_id=6):
    servo_485 = Servo(server485_id)
    servo = ServoPWM(servopwm_id)
    servo.servocontrol(180, 25)
    time.sleep(1)
    servo_485.servocontrol(-10, 50)
    time.sleep(1)
    servo.servocontrol(120, 100)
    time.sleep(3)
    servo.servocontrol(180, 25)
    time.sleep(3)
    servo_485.servocontrol(35, 35)
    time.sleep(3)


if __name__ == '__main__':
    time.sleep(4)
    # servo = ServoPWM(6)
    # servo.servocontrol(115, 25)
    # time.sleep(1)
    # s = Servo(2)
    # s.servocontrol(35, 100)
    # time.sleep(5)
    # capture_target()
    # take_barracks()
    # s = ServoPWM(6)
    # s.servocontrol(180, 100)
    transport_forage()
    # change_camera_direction(2, 'left')
    # raise_flag(5)
    # time.sleep(1)
    # shot_target(2)
    # time.sleep(1)