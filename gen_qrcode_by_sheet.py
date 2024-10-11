import os
import sys
import uuid

import pandas as pd

from src.app.qrcode_helper import QRCodeHelper
from src.app.google_sheet_helper import GoogleSheetHelper
from config import config

ROOT_DIR = os.getcwd()


def main(saved_format="csv"):
    # 透過憑證連接 google sheet
    service_file = config["GOOGLE_SHEET_KEY"]
    url = config["GOOGLE_SHEET_URL"]
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
    qr_data_pd = data[item_list].copy()

    # Add a unique_id column to the DataFrame
    qr_data_pd.loc[:, 'unique_id'] = [str(uuid.uuid4()) for _ in range(len(qr_data_pd))]

    # 2. generate qr code
    for index, row in qr_data_pd.iterrows():
        # Use the generated unique_id from the DataFrame
        unique_id = row['unique_id']
        email = row[column_titles[1]]
        chinese_name = row[column_titles[4]]
        english_name = row[column_titles[5]]
    
        # Create QR data text
        qr_data = f"id: {unique_id}\n姓名: {chinese_name}\n英文: {english_name}\n信箱: {email}"

        # Define the output file name and path
        output_file = f"{index+1}_{english_name}_qrcode.png"
        output_dir = f"{ROOT_DIR}/datas"

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # 生成 QR Code
        qrcode_generator.generate(qr_data, output_file=output_file, output_dir=output_dir)

    # Add a 'scanned' column to the DataFrame 
    qr_data_pd.loc[:, 'scanned'] = False  # Default scanned column

    if saved_format == "xlsx":
        # Save DataFrame to an Excel file
        # index=False prevents writing row numbers
        qr_data_pd.to_excel('報名資料.xlsx', index=True)
    else:
        # Save DataFrame to a CSV file
        qr_data_pd.to_csv('報名資料.csv', index=False)


if __name__ == "__main__":
    main(saved_format="xlsx")
