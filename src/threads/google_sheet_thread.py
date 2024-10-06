import os

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QVariant

from src.app.google_sheet_helper import GoogleSheetHelper


class GoogleSheetThread(QObject):
    dumpSig = pyqtSignal(str, str, str, arguments=[
                         'id', 'name', 'email'])
    dumpDone = pyqtSignal()

    def __init__(self, service_file, url, parent=None):
        super(GoogleSheetThread, self).__init__(parent)

        # initialize GoogleSheetHelper
        self.gs = GoogleSheetHelper(service_file=service_file, url=url)

    @pyqtSlot(int)
    def get_all_data(self, index):
        """ Get Sheet Data Thread Start """
        print("Get Sheet Data Thread Start")
        index = 0 if not index else index
        self.gs.select_worksheet_by_index(index) # default index is 0
        data = self.gs.read_all()

        # 1. processing data: only need email, chinese_name, english_name
        column_titles = data.columns.tolist()
        item_list = [column_titles[1], column_titles[4], column_titles[5]]
        qr_data_pd = data[item_list]

        for index, row in qr_data_pd.iterrows():
            email = row[column_titles[1]]
            chinese_name = row[column_titles[4]]
            english_name = row[column_titles[5]]
            # qr_data = f"姓名: {chinese_name}\n英文: {english_name}\n信箱: {email}"
            # output_file = f"{index+1}_{english_name}_qrcode.png"

            self.dumpSig.emit(str(index), chinese_name, email)
        self.dumpDone.emit()
