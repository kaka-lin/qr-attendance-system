import os
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

import pygsheets
import pandas as pd
from config import config


class GoogleSheetHelper:
    def __init__(self, service_file, url):
        # authorization
        self.gs = pygsheets.authorize(service_file=service_file)
        self.sht = self.gs.open_by_url(url)
        
        # 讀取全部工作表
        self.wks_list = self.sht.worksheets()
    
    def select_worksheet_by_index(self, index=0):
        # 選取工作表 by index
        self.wks = self.sht[index]
    
    def select_worksheet_by_title(self, title):
        # 指定工作表 by 名稱
        self.wks = self.sht.worksheet_by_title(title)

    def read_cell(self, position="A1"):
        return self.wks.cell(position).value
    
    def read_all(self, start='A1', index_colum=0, empty_value='', include_tailing_empty=False):
        # pd.DataFrame(wks.get_all_records())
        return self.wks.get_as_df(start=start, index_colum=index_colum, empty_value=empty_value, include_tailing_empty=include_tailing_empty)

    def export(self, file_format=pygsheets.ExportType.CSV, filename='test', path=''):
        self.wks.export(file_format=file_format, filename=filename, path=path)


if __name__ == "__main__":
    # 透過憑證連接 google sheet
    service_file = config["google_sheet_key"]
    url = config["google_sheet_url"]
    gs = GoogleSheetHelper(service_file=service_file, url=url)
   
    # 選取工作表
    gs.select_worksheet_by_index(0)

    # 讀取全部資料
    print(gs.read_all())
