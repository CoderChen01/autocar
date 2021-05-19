import sys
import datetime
import time
import cv2
import configs
from widgets import Button
from tasks import light_work
from improved_videocapture import BackgroundVideoCapture
from driver import Driver, SLOW_DOWN_RATE

if __name__ == '__main__':
    # TODO 我打算先使用串行方式编码调试效果，
    #  模型返回结果为detectors.DetectionResult类
    start_button = Button(1, 'UP')
    stop_button = Button(1, 'DOWN')
    front_camera = BackgroundVideoCapture(0)
    driver = Driver()
    front_camera.start()
    # 基准速度
    driver.set_speed(35)
    # 转弯系数
    driver.cart.Kx = 0.95
    # 延时
    time.sleep(0.5)
    while True:
        if start_button.clicked():
            time.sleep(0.3)
            break
        print("Wait for start!")
    while True:
        _, front_image = front_camera.read()
        driver.go(front_image)
        if stop_button.clicked():
            print("End of program!")
            break
    driver.stop()
    front_camera.stop()
