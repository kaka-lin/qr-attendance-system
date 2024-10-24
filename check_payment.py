import os
import pandas as pd

from src.threads.google_sheet_thread import GoogleSheetThread
from config import config


def preprocess_attendance_data(data):
    # 1. processing data: only need email, chinese_name, english_name, rotaract_club, account number 
    column_titles = data.columns.tolist()
    item_list = [column_titles[1], column_titles[4], column_titles[5], column_titles[2], column_titles[11], column_titles[9], column_titles[10]]
    attendance_data_df = data[item_list].copy()

    # 2. Add a unique_id column to the DataFrame
    attendance_data_df.loc[:, 'rotaract_club'] = attendance_data_df.apply(
        lambda row: row[column_titles[2]] if row[column_titles[2]] != '其他友社及來賓' else row[column_titles[11]]+"來賓", axis=1)    
    attendance_data_df.loc[:, 'account_number'] = attendance_data_df.apply(
        lambda row: row[column_titles[9]] if row[column_titles[9]] != '' else row[column_titles[10]], axis=1)
    attendance_data_df.loc[:, 'Payment amount'] = attendance_data_df.apply(
        lambda row: '800' if row[column_titles[9]] != '' else '1200', axis=1)

    attendance_data_df = attendance_data_df.drop(columns=[column_titles[2], column_titles[11], column_titles[9], column_titles[10]])

    return attendance_data_df


def preprocess_payment_data(data):
    # 1. processing data: only need 存入, 備註/資金用途
    column_titles = data.columns.tolist()
    item_list = [column_titles[4], column_titles[7]]

    # 將 DataFrame 中的所有 '\n' 和 '\t' 替換為空字符串, 
    payment_data_df = data[item_list].copy().replace({'\n': '', '\t': ''}, regex=True)
    payment_data_df[item_list[1]] = payment_data_df[item_list[1]].str.replace(r'[^\d]', '', regex=True)
    
    #然後針對特定的 column_titles[7] 列進行非數字字符過濾, 且只要後五碼
    payment_data_df["account_number"] = payment_data_df[item_list[1]].str[-5:]

    # strip()
    payment_data_df = payment_data_df.rename(columns={column_titles[4]: column_titles[4].strip()})
    return payment_data_df


def check_payment(attendance_data_df, payment_data_df):
    # 將 account_number 列轉換為字符串類型以進行匹配
    attendance_data_df['account_number'] = attendance_data_df['account_number'].astype(str)
    payment_data_df['account_number'] = payment_data_df['account_number'].astype(str)

    # 使用 account_number 作為鍵來進行合併
    # left: 左連接（Left Join） 操作，返回左表中所有的行，以及右表中那些與左表中行匹配的行
    # outer: 外連接（Outer Join） 操作，返回兩個表中所有的行，如果匹配不到的行，則用 NaN 填充
    merged_df = pd.merge(attendance_data_df, payment_data_df, on='account_number', how='left', suffixes=('_att', '_pay'))
    # column_titles = merged_df.columns.tolist()
    # print(merged_df)

    # 檢查每個會員是否有匯款，並且金額是否匹配
    merged_df['匯款狀態'] = merged_df['Payment amount'] == merged_df['存入']

    # 如果匯款金額錯誤，標記為 False，正確則標記為 True
    merged_df['匯款金額正確'] = (merged_df['Payment amount'] == merged_df['存入'])

    # 顯示匯款狀態與金額是否正確的結果
    # result_df = merged_df[['中文姓名', 'account_number', 'Payment amount', '存入', '匯款狀態', '匯款金額正確']]

    # 打印結果
    # print(result_df)

    # save to xlsx
    merged_df.to_excel('匯款檢查結果.xlsx', index=True)


def main():
    service_file = config["GOOGLE_SHEET_KEY"]
    url = config["GOOGLE_SHEET_URL"]
    db = None

    # 讀取報名資料
    google_sheet_thread = GoogleSheetThread(service_file, url, db)
    data = google_sheet_thread.get_all_data(0)
    attendance_data_df = preprocess_attendance_data(data)
    # print(attendance_data_df)

    # 讀取付款資料
    payment_data_df = pd.read_csv('往來明細.csv')
    payment_data_df = preprocess_payment_data(payment_data_df)
    payment_data_df.to_csv('匯款結果.csv', index=False)
    # print(payment_data_df)
    
    # 檢查付款
    check_payment(attendance_data_df, payment_data_df)


if __name__ == "__main__":
    main()
