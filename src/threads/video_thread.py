import time

import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from src.app.qrcode_helper import QRCodeHelper


class VideoThread(QObject):
    """ This thread is capture video with opencv """
    frameReady = pyqtSignal(np.ndarray)
    finished = pyqtSignal(str)

    def __init__(self, camera_port=0, parent=None):
        super(VideoThread, self).__init__(parent)

        self.camera_port = camera_port
        self.running = False

        self.qrcode = QRCodeHelper()

    @pyqtSlot()
    def start(self):
        print("Start Video Thread, camera_port:", self.camera_port)
        self.cap = cv2.VideoCapture(self.camera_port)
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        self.running = True
        while self.running:
            ret, frame = self.cap.read()

            if not ret:
                print("Can't receive frame (stream end?)")
                break
            
            # convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            decoded_image = self.qrcode.decode(frame)
            self.frameReady.emit(frame)
        
        self.cap.release()
        self.finished.emit("OpenCV")
    
    def stop(self):
        self.running = False
