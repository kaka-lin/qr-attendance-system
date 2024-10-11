import os
import uuid

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant

from src.app.google_sheet_helper import GoogleSheetHelper
from src.app.qrcode_helper import QRCodeHelper
from src.app.mongo_controller import MongoController


class GoogleSheetThread(QObject):
    sheetDumpSig = pyqtSignal(str, str, str, str, arguments=[
        'id', 'chinese_name', 'english_name', 'email'])
    genQRCodeSheetDone = pyqtSignal()

    def __init__(self, service_file, url, db, parent=None):
        super(GoogleSheetThread, self).__init__(parent)

        # initialize GoogleSheetHelper
        self.gs = GoogleSheetHelper(service_file=service_file, url=url)

        self.db = db
        self.qrcode_generator = QRCodeHelper(db=self.db)

        self.output_dir = os.environ["ROOT_DIR"] + "/images"

    @pyqtSlot(int)
    def generate_code_sheet(self, index):
        """ Get Sheet Data and Generate QRCode Thread Start """
        print("Get Sheet Data and Generate QRCode Thread Start")
        
        index = 0 if not index else index
        data = self.get_all_data(index)
        
        # 1. processing data: only need email, chinese_name, english_name
        column_titles = data.columns.tolist()
        item_list = [column_titles[1], column_titles[4], column_titles[5]]
        qr_data_pd = data[item_list].copy()

        # 2. Add a unique_id column to the DataFrame
        qr_data_pd.loc[:, 'unique_id'] = [str(uuid.uuid4()) for _ in range(len(qr_data_pd))]
        qr_data_pd.loc[:, 'scanned'] = False

        # 3. Save the data to MongoDB
        qr_data_dict = qr_data_pd.to_dict(orient='records')
        self.db.create_or_update_many(qr_data_dict)

        # generate qr code and emit signal to update UI
        for index, row in qr_data_pd.iterrows():
            # Use the generated unique_id from the DataFrame
            unique_id = row['unique_id']
            email = row[column_titles[1]]
            chinese_name = row[column_titles[4]]
            english_name = row[column_titles[5]]

            # Create QR data text
            qr_data = f"unique_id: {unique_id}\n姓名: {chinese_name}\n英文: {english_name}\n信箱: {email}"
            output_file = f"{index+1}_{english_name}_qrcode.png"

            self.generate_qrcode(qr_data, output_file, self.output_dir)
            self.sheetDumpSig.emit(str(index+1), chinese_name, str(english_name), email)
        self.genQRCodeSheetDone.emit()
    
    def get_all_data(self, index):
        # print("Get All Data")
        self.gs.select_worksheet_by_index(index) # default index is 0
        data = self.gs.read_all()
        return data

    def generate_qrcode(self, qr_data, output_file, output_dir):
        # print("Generate QRCode with Google Sheet Data")
        self.qrcode_generator.generate(qr_data, output_file=output_file, output_dir=output_dir)
