from generate_qrcode import QRCodeGenerator
from google_sheet import GoogleSheetHelper

from config.dev import config


def main():
    # 透過憑證連接 google sheet
    service_file = config["google_sheet_key"]
    url = config["google_sheet_url"]
    gc = GoogleSheetHelper(service_file=service_file, url=url)
    qrcode_generator = QRCodeGenerator()
    
    # 選取工作表
    gc.select_worksheet_by_index(0)

    # 讀取全部資料
    data = gc.read_all()

    # 生成 QR Code
    # 1. processing data: only need email, chinese_name, english_name
    column_titles = data.columns.tolist()
    item_list = [column_titles[1], column_titles[4], column_titles[5]]
    qr_data_pd = data[item_list]

    # 2. generate qr code
    for index, row in qr_data_pd.iterrows():
        email = row[column_titles[1]]
        chinese_name = row[column_titles[4]]
        english_name = row[column_titles[5]]
        # print(index, email, chinese_name, english_name)
        qr_data = f"Chinese Name: {chinese_name}\nEnglish Name: {english_name}\nEmail: {email}" 
        output_file = f"{index+1}_{english_name}_qrcode.png"

        # 生成 QR Code
        qrcode_generator.generate(qr_data, output_file=output_file)


if __name__ == "__main__":
    main()
