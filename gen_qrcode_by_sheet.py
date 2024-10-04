import os
import sys

from src.app.qrcode_helper import QRCodeHelper
from src.app.google_sheet_helper import GoogleSheetHelper
from config import config

ROOT_DIR = os.getcwd()


def main():
    # 透過憑證連接 google sheet
    service_file = config["google_sheet_key"]
    url = config["google_sheet_url"]
    gs = GoogleSheetHelper(service_file=service_file, url=url)
    qrcode_generator = QRCodeHelper()
    
    # 選取工作表
    gs.select_worksheet_by_index(0)

    # 讀取全部資料
    data = gs.read_all()
    
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
        # qr_data = '\n'.join(key + ": " + str(val) for key, val in row.items())
        qr_data = f"姓名: {chinese_name}\n英文: {english_name}\n信箱: {email}"
        output_file = f"{index+1}_{english_name}_qrcode.png"

        # 生成 QR Code
        qrcode_generator.generate(qr_data, output_file=output_file, output_dir=f"{ROOT_DIR}/images")


if __name__ == "__main__":
    main()
