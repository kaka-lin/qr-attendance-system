import os
import uuid
import json

import cv2
import qrcode
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot


class QRCodeHelper(QObject):
    decodeMsgSig = pyqtSignal(str, bool)

    def __init__(self, 
                 version=None, 
                 error_correction=qrcode.constants.ERROR_CORRECT_L,
                 box_size=10,
                 border=4,
                 db=None,
                 parent=None): 
        super(QRCodeHelper, self).__init__(parent)   
        # 創建 QR Code
        #   - version: Controls the size of the QR code, 
        #              from 1 to 40, 1: 21x21, 40: 177x177, or None for automatic
        self.qr = qrcode.QRCode(
            version=version,  # Controls the size of the QR code
            error_correction=error_correction,  # Error correction level
            box_size=box_size,  # Size of each box in pixels
            border=border,  # Border size
        )

        self.qrcode_detector = cv2.QRCodeDetector()   
        self.db = db
    
    def generate(self, data, output_file="qrcode.png", output_dir="images"):
        if data is None or data == "":
            return

        # Add data to the QR code
        self.qr.clear()  # Clear the QR code data
        self.qr.add_data(data)
        self.qr.make(fit=True)

        # Generate the QR code image
        img = self.qr.make_image(fill='black', back_color='white')

        # Save the QR code image to a file
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        image_path = os.path.join(output_dir, output_file)
        img.save(image_path)
        print(f"QR code saved to {image_path}")
        return image_path
    
    def decode(self, image):   
        decoded_data, points, _ = self.qrcode_detector.detectAndDecode(image)
        if decoded_data:
            # print(f"QR Code detected: \n{decoded_text}")
            # 畫出 QR Code 的邊框
            # points 是一個形狀為 (1, 4, 2) 的 NumPy 數組，其中：
            # - 1: 代表 QR Code 檢測到的數量（如果檢測到多個 QR Code，這個數量會增加）。
            # - 4: 代表 QR Code 的四個角點（四個點形成一個四邊形，對應 QR Code 的邊界）。
            # - 2: 代表每個點的 (x, y) 座標值。
            if points is not None and len(points) > 0:
                points = points[0]  # points 是一個多維數組，需要先提取第一個元素
                # 使用 cv2.rectangle 繪製 QR Code 邊框
                top_left = (int(points[0][0]), int(points[0][1]))
                bottom_right = (int(points[2][0]), int(points[2][1]))
                cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

            decoded_list = decoded_data.strip().split("\n")
            data_dict = dict(data.split(": ") for data in decoded_list)
            self.query_filter = {'unique_id': data_dict['unique_id']}
            
            isScanned = False
            if self.db:
                data, isFound = self.db.query(self.query_filter)
                if isFound:
                    if data['scanned'] == False:
                        self.db.update(self.query_filter, {'$set': {'scanned': True}})
                    else:
                        isScanned = True

            # 將解碼的資料傳送給 UI
            self.decodeMsgSig.emit(decoded_data, isScanned)
        else:
            self.decodeMsgSig.emit("", False)
            
        return image, decoded_data


if __name__ == "__main__":
    chinese_name = "林家豪"
    english_name = "Kaka"
    email = "vn503024@gmail.com"
    output_dir = "images"
    output_file = "qrcode.png"

    qr_data = f"姓名: {chinese_name}\n英文: {english_name}\n信箱: {email}"

    # 生成 QR Code
    qrcode_generator = QRCodeHelper()
    qrcode_generator.generate(qr_data, output_file=output_file)

    # 解碼 QR Code
    # Load the QR code image
    image_path = os.path.join(output_dir, output_file)
    qr_image = cv2.imread(image_path)
    decoded_image, decoded_data = qrcode_generator.decode(qr_image)

    decoded_data = decoded_data.strip().split("\n")
    data_dict = dict(data.split(": ") for data in decoded_data)
    print(data_dict)

    # Display the decoded image
    plt.imshow(cv2.cvtColor(decoded_image, cv2.COLOR_BGR2RGB))
    plt.show()
