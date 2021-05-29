import sys
import datetime
import time
import cv2
import configs
from widgets import Button
from tasks import light_work
from improved_videocapture import BackgroundVideoCapture
from driver import Driver, SLOW_DOWN_RATE
from detectors import SignDetector, TaskDetector
SIGN_DETECTOR = SignDetector()
TASK_DETECTOR = TaskDetector()


if __name__ == '__main__':
    start_button = Button(1, 'UP')
    stop_button = Button(1, 'DOWN')
    front_camera = BackgroundVideoCapture(0)
    driver = Driver()
    # 基准速度
    driver.set_speed(30)
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
        SIGN_DETECTOR.detect(front_image)
        if stop_button.clicked():
            print("End of program!")
            break
    driver.stop()
    front_camera.close()
