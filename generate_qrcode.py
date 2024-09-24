import os
import qrcode

class QRCodeGenerator:
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
    
    def generate(self, data, output_dir="images", output_file="qrcode.png"):
        if data is None or data == "":
            return
        
        # Add data to the QR code
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


if __name__ == "__main__":
    name = "Kaka Lin"
    email = "vn503024@gmail.com"
    output_dir = "images"
    output_file = "qrcode_kaka.png"

    # 將姓名和信箱等資訊组合成字串
    data = f"Name: {name}\nEmail: {email}"

    # 生成 QR Code
    qrcode_generator = QRCodeGenerator()
    qrcode_generator.generate(data)
