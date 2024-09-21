import io
import qrcode


def generate_qr_code(name, email, output_file):
    # 將姓名和信箱等資訊组合成字串
    data = f"Name: {name}\nEmail: {email}"

    # 創建 QR Code
    #   - version: Controls the size of the QR code, 
    #              from 1 to 40, 1: 21x21, 40: 177x177, or None for automatic
    qr = qrcode.QRCode(
        version=None,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in pixels
        border=4,  # Border size
    )
    
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill='black', back_color='white')

    # 保存生成的 QR 码到文件
    img.save(output_file)
    print(f"QR code saved to {output_file}")


if __name__ == "__main__":
    name = "Kaka Lin"
    email = "vn503024@gmail.com"
    output_file = "qrcode_kaka.png"

    generate_qr_code(name, email, output_file)
