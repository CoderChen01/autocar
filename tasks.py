import time

from widgets import *


def buzzing():
    buzzer = Buzzer()
    for _ in range(10):
        buzzer.rings()
        time.sleep(0.5)


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


def raise_flag(motor_prot, magneto_port):
    motor = MotorRotate(motor_prot)
    magneto = MagnetoSensor(magneto_port)
    motor.motor_rotate(-12)
    while True:
        data = magneto.read()
        if data is None:
            continue
        if data > 80:
            motor.motor_rotate(0)
            break
    light_work(2, 'green')
    light_work(2, 'off')
    light_work(2, 'green')
    light_work(2, 'off')
    light_work(2, 'green')
    light_work(2, 'off')
    motor.motor_rotate(-10)
    motor.motor_rotate(0)


def shot_target(motor_port):
    print("shot_target start!")
    setmotor1 = MotorRotate(motor_port)
    time.sleep(0.5)
    for _ in range(2):
        setmotor1.motor_rotate(40)
        time.sleep(0.5)
        setmotor1.motor_rotate(0)
        time.sleep(0.3)
        setmotor1.motor_rotate(-60)
        setmotor1.motor_rotate(0)
        time.sleep(1)
    print("shot_target stop!")


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
    servo1.servocontrol(-85,servo1speed)
    time.sleep(2)


def transport_forage(motor_port):
    print("transport_forage start!")
    setmotor1 = MotorRotate(motor_port)
    time.sleep(0.5)
    setmotor1.motor_rotate(10)
    time.sleep(1.5)
    setmotor1.motor_rotate(0)
    time.sleep(0.2)
    setmotor1.motor_rotate(-20)
    time.sleep(0.2)
    setmotor1.motor_rotate(0)
    print("transport_forage stop!")


def take_barracks():
    driver = Driver()
    driver.set_speed(driver.full_speed)
    driver.set_Kx(0.8)
    driver.stop()
    time.sleep(0.5)
    driver.driver_run(20, 19)
    time.sleep(3.4)
    driver.driver_run(-8, -18)
    time.sleep(3.4)
    driver.driver_run(-18, -8)
    time.sleep(3.0)
    driver.stop()
    for _ in range(4):
        light_work(2, 'red')
        time.sleep(0.2)
        light_work(2, 'off')
    driver.driver_run(18, 8)
    time.sleep(2.8)
    driver.driver_run(18, 18)
    time.sleep(0.6)
    driver.driver_run(8, 18)
    time.sleep(2.8)
    driver.stop()


if __name__ == '__main__':
    raise_flag(3, 3)