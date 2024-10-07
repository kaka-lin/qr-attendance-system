import time

import cv2
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class VideoThread(QObject):
    """ This thread is capture video with opencv """
    frameReady = pyqtSignal(np.ndarray)
    framefinished = pyqtSignal()

    def __init__(self, camera_port=0, parent=None):
        super(VideoThread, self).__init__(parent)

        self.camera_port = camera_port
        self.running = False

    @pyqtSlot()
    def start(self):
        print("Start Video Thread")
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
            self.frameReady.emit(frame)
        
        self.cap.release()
        cv2.destroyAllWindows()
        self.framefinished.emit()
    
    def stopVideo(self):
        self.running = False
