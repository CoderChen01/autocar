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
        light_work(2, 'red')
        time.sleep(1)
        light_work(2, 'off')
        time.sleep(0.5)
    servo.servocontrol(0, 100)
    time.sleep(0.5)


def shot_target(motor_port):
    setmotor1 = MotorRotate(motor_port)
    time.sleep(0.5)
    for _ in range(2):
        setmotor1.motor_rotate(70)
        time.sleep(0.6)
        setmotor1.motor_rotate(0)
        time.sleep(0.3)
        setmotor1.motor_rotate(-70)
        time.sleep(0.5)
        setmotor1.motor_rotate(0)
        time.sleep(1)


def capture_target(servo_485_id, servo_pwm_id):
    servo1 = Servo(servo_485_id)
    servo2 = ServoPWM(servo_pwm_id)
    servo1speed = 100
    servo2speed = 50
    time.sleep(1)
    servo2.servocontrol(100, servo2speed)
    time.sleep(2)
    servo1.servocontrol(10, 60)
    time.sleep(2)
    servo2.servocontrol(180, servo2speed)
    time.sleep(2)
    servo1.servocontrol(-80,servo1speed)
    time.sleep(2)


def transport_forage(server485_id, servopwm_id):
    servo_485 = Servo(server485_id)
    servo = ServoPWM(servopwm_id)
    servo.servocontrol(170, 25)
    time.sleep(1)
    servo_485.servocontrol(-10, 50)
    time.sleep(1)
    servo.servocontrol(70, 25)
    time.sleep(3)
    servo.servocontrol(170, 25)
    time.sleep(3)
    servo_485.servocontrol(35, 35)
    time.sleep(2)


def take_barracks():
    driver = Driver()
    driver.driver_run(5, 20)
    time.sleep(2)
    driver.driver_run(10, 10)
    time.sleep(2.5)
    driver.driver_run(20, 5)
    time.sleep(2)
    driver.stop()
    for _ in range(3):
        light_work(2, 'red')
        time.sleep(1)
        light_work(2, 'off')
        time.sleep(0.5)
    driver.driver_run(-10, -10)
    time.sleep(2)
    driver.driver_run(20, 5)
    time.sleep(2)
    driver.driver_run(10, 10)
    time.sleep(2)
    driver.driver_run(5, 20)
    time.sleep(1)


if __name__ == '__main__':
    time.sleep(4)
    # s = Servo(2)
    # s.servocontrol(35, 100)
    # time.sleep(5)
    transport_forage(2, 6)
    # s = ServoPWM(6)
    # s.servocontrol(180, 100)
    # transport_forage(1)
    # change_camera_direction(2, 'left')
    # raise_flag(5)
    # time.sleep(1)
    # shot_target(2)
    # time.sleep(1)