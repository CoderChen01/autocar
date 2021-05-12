import threading
import time

import cv2


class Camera:
    def __init__(self, src=0, width=640, height=480):
        self.src = src
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_FPS, 15)
        self.stopped = False
        for _ in range(10):  # warm up the camera
            (self.grabbed, self.frame) = self.stream.read()

    def start(self):
        threading.Thread(target=self.update).start()

    def update(self):
        count = 0
        while True:
            if self.stopped:
                return
            self.grabbed, self.frame = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()
