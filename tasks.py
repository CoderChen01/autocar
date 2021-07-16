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
        buzzing(1)
        time.sleep(1)
        light_work(2, 'off')
        time.sleep(1)
    servo.servocontrol(30, 100)
    time.sleep(0.5)


def shot_target(motor_port=2):
    setmotor1 = MotorRotate(motor_port)
    time.sleep(0.5)
    setmotor1.motor_rotate(100)
    time.sleep(0.6)
    setmotor1.motor_rotate(0)
    time.sleep(1)
    setmotor1.motor_rotate(-100)
    time.sleep(0.6)
    setmotor1.motor_rotate(0)
    time.sleep(1)


def take_barracks(driver):
    driver.driver_run(20, 0, 1.7)
    driver.driver_run(-15, -15, 4.5)
    driver.driver_run(0, 20, 1.7)
    for _ in range(3):
        light_work(2, 'red')
        buzzing(1)
        light_work(2, 'off')
        time.sleep(0.5)
    driver.driver_run(-15, -15, 1.5)
    driver.driver_run(20, 0, 1.7)
    driver.driver_run(10, 10, 1.5)
    driver.driver_run(5, 20, 2)


def capture_target(servo_485_id=1, servo_pwm_id=2):
    servo1 = Servo(servo_485_id)
    servo2 = ServoPWM(servo_pwm_id)
    servo1.servocontrol(-45, 50)
    time.sleep(1)
    servo2.servocontrol(90, 100)
    time.sleep(2)
    servo1.servocontrol(-15, 50)
    time.sleep(1)
    servo2.servocontrol(180, 100)
    time.sleep(2)
    servo1.servocontrol(-80,60)
    time.sleep(2)


def transport_forage(server485_id=2, servopwm_id=6):
    servo_485 = Servo(server485_id)
    servo = ServoPWM(servopwm_id)
    servo_485.servocontrol(-10, 50)
    time.sleep(1)
    servo.servocontrol(145, 100)
    time.sleep(3)
    servo.servocontrol(90, 25)
    time.sleep(3)
    servo_485.servocontrol(35, 35)
    time.sleep(3)


if __name__ == '__main__':
    time.sleep(4)
    raise_flag(3)
    # shot_target()
    # servo = ServoPWM(6)
    # servo.servocontrol(115, 25)
    # time.sleep(1)
    # s = Servo(2)
    # s.servocontrol(35, 100)
    # time.sleep(5)
    # capture_target()
    # take_barracks()
    # s = ServoPWM(6)
    # s.servocontrol(0, 100)
    # time.sleep(1)
    # s.servocontrol(70, 100)
    # transport_forage()
    # time.sleep(2)
    # transport_forage()
    # time.sleep(2)
    # transport_forage()
    # change_camera_direction(2, 'left')
    # raise_flag(5)
    # time.sleep(1)
    # shot_target(2)
    # time.sleep(1)
