import os
import time

import cv2
import numpy as np
import pygame
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from src.app.qrcode_helper import QRCodeHelper


class VideoThread(QObject):
    """ This thread is capture video with opencv """
    frameReady = pyqtSignal(np.ndarray)
    finished = pyqtSignal(str)

    decodeMsgSig = pyqtSignal(bool, str, bool)

    def __init__(self, camera_port=0, db=None, parent=None):
        super(VideoThread, self).__init__(parent)

        self.root_path = os.environ["ROOT_DIR"]
        self.beep_mp3_path = os.path.join(self.root_path, "data/beep.mp3")

        self.camera_port = camera_port
        self.running = False
        self.last_decoded_data = None
        self.cooldown = 5  # 設置冷卻時間 (秒)
        self.last_scan_time = 0  # 上次成功掃描的時間

        self.db = db
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
            frame, decoded_data = self.qrcode.decode(frame)

            # 如果掃描結果與上次不同且超過冷卻時間
            if decoded_data:
                if self.is_new_qr_code(decoded_data) or time.time() - self.last_scan_time > self.cooldown:
                    # print(f"QR Code Scanned: {decoded_data}")
                    self.last_decoded_data = decoded_data  # 更新最近掃描到的 QR code
                    self.last_scan_time = time.time()  # 更新掃描時間
                    self.play_beep_sound()  # 播放逼一聲音效
                    self.check_scanned(decoded_data)

            self.frameReady.emit(frame)
        
        self.cap.release()
        self.finished.emit("OpenCV")
    
    def stop(self):
        self.running = False
    
    def check_scanned(self, decoded_data):
        isDetected = False
        isScanned = False

        if decoded_data:
            isDetected = True

            decoded_list = decoded_data.strip().split("\n")
            data_dict = dict(data.split(": ") for data in decoded_list)
            self.query_filter = {'unique_id': data_dict['unique_id']}

            if self.db:
                data, isFound = self.db.query(self.query_filter)
                if isFound:
                    if data['scanned'] == False:
                        self.db.update(self.query_filter, {'$set': {'scanned': True}})
                    else:
                        isScanned = True
   
            self.decodeMsgSig.emit(isDetected, decoded_data, isScanned)
        else:
            self.decodeMsgSig.emit(isDetected, "", isScanned)
    
    def is_new_qr_code(self, decoded_data):
        return decoded_data != self.last_decoded_data
    
    def play_beep_sound(self):
        """ 使用 pygame 播放音效 """
        pygame.mixer.init()
        pygame.mixer.music.load(self.beep_mp3_path)
        pygame.mixer.music.play()

        # 等待音樂播放完畢再繼續
        # while pygame.mixer.music.get_busy():
        #     pygame.time.Clock().tick(10)
