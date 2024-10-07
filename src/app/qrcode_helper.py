import os
import uuid

import cv2
import qrcode
from pyzbar import pyzbar
import matplotlib.pyplot as plt


class QRCodeHelper:
    def __init__(self, 
                 version=None, 
                 error_correction=qrcode.constants.ERROR_CORRECT_L,
                 box_size=10,
                 border=4):    
        # 創建 QR Code
        #   - version: Controls the size of the QR code, 
        #              from 1 to 40, 1: 21x21, 40: 177x177, or None for automatic
        self.qr = qrcode.QRCode(
            version=version,  # Controls the size of the QR code
            error_correction=error_correction,  # Error correction level
            box_size=box_size,  # Size of each box in pixels
            border=border,  # Border size
        )
    
    def generate(self, data, output_file="qrcode.png", output_dir="images"):
        if data is None or data == "":
            return

        # generate unique id
        unique_id = str(uuid.uuid4())
        # Add unique data (Assume it points to some URL) to the data
        unique_data = f"http://example.com/scan/{unique_id}"
        data = f"{data}\nunique_id: {unique_data}"

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
    
    def decode(self, image_path):
        # Load the QR code image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Unable to open image: {image_path}")
            return None
        
        # Using pyzbar to decode the QR code image
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            qr_type = obj.type
            qr_data = obj.data.decode('utf-8')
        
            print(f"Type: {qr_type}")
            print(f"Data: {qr_data}")

            # 在圖像上繪製邊框
            (x, y, w, h) = obj.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 顯示帶有 QR Code 的影像
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.show()
        return qr_data


if __name__ == "__main__":
    name = "Kaka Lin"
    email = "vn503024@gmail.com"
    output_dir = "images"
    output_file = "qrcode_kaka.png"

    # 將姓名和信箱等資訊组合成字串
    data = f"Name: {name}\nEmail: {email}"

    # 生成 QR Code
    qrcode_generator = QRCodeHelper()
    qrcode_generator.generate(data, output_file=output_file)

    # 解碼 QR Code
    qr_data = qrcode_generator.decode(os.path.join(output_dir, output_file))
