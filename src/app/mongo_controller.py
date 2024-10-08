import os
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)
from typing import List, Dict

from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidURI, OperationFailure, BulkWriteError

from config import config


class MongoController(QObject):
    def __init__(self, uri, parent=None):
        super(MongoController, self).__init__(parent)

        self.uri = uri
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            print("Connected to MongoDB successfully")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.client = None  # 確保連接失敗後不允許後續操作
        except InvalidURI as e:
            print(f"Invalid MongoDB URI: {e}")
            self.client = None  # 無效 URI
        except Exception as e:
            print(f"An unexpected error occurred during connection: {e}")
            self.client = None
    
    @pyqtSlot(str, str)
    def choose_collection(self, db_name, collection_name):
        if self.client is None:
            print("Error: Not connected to MongoDB. Please connect first.")
            return

        try:
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"Connected to database: {db_name}, collection: {collection_name}")
            
            # 為指定的 key 創建唯一索引
            self.collection.create_index([('中文姓名', 1), ('電子郵件地址', 1)], unique=True)
            print("Index created successfully")
        except OperationFailure as e:
            print(f"Failed to select database or collection: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def create(self, data: Dict):
        try:
            result = self.collection.insert_one(data)
        except Exception as e:
            print(f"Failed to insert documents: {e}")
    
    def create_many(self, data: List[Dict]):        
        try:
            result = self.collection.insert_many(data, ordered=False)
            print(f"Inserted {len(result.inserted_ids)} documents successfully")
        except BulkWriteError as bwe:
            # 獲取並處理批量寫入錯誤
            # print("Failed to insert multiple documents: batch op errors occurred.")
            # for error in bwe.details['writeErrors']:
            #     print(f"Error {error['code']}: {error['errmsg']}")
            #     print(f"Duplicate key: {error['keyValue']}")
            pass
        except Exception as e:
            print(f"An error occurred: {e}")

    def query(self, query_filter):
        try:
            result = self.collection.find(query_filter)
            documents = list(result)  # 將結果轉換為列表
            for doc in documents:
                print(doc)
            return documents
        except Exception as e:
            print(f"Failed to query documents: {e}")
            return None
    
    def query_all(self):
        try:
            result = self.collection.find()
            documents = list(result)  # 將結果轉換為列表
            for doc in documents:
                print(doc)
            return documents
        except Exception as e:
            print(f"Failed to query all documents: {e}")
            return None

    def delete(self, query_filter):
        try:
            result = self.collection.delete_many(query_filter)
            print(f"Deleted {result.deleted_count} documents")
        except Exception as e:
            print(f"Failed to delete documents: {e}")
    @pyqtSlot()
    def close(self):
        if self.client:
            self.client.close()
            print("Connection to MongoDB closed")


if __name__ == "__main__":
    # 初始化 MongoController，連接到 MongoDB Atlas 集群
    uri = config["MONGO_URI"]
    db_name = "test_database"
    collection_name = "test_collection"
    
    mongo_controller = MongoController(uri)

    # 連接到 MongoDB 集群
    mongo_controller.connect()
    # 選擇資料庫和集合
    mongo_controller.choose_collection(db_name, collection_name)

    # 插入一個文檔
    item_1 = {
        "name": "Kaka Lin", 
        "email": "vn503024@gmail.com"
    }
    mongo_controller.create(item_1)

    # 查詢所有文檔
    mongo_controller.query_all()

    # 查詢特定條件的文檔
    query_filter = {"name": "Kaka Lin"}
    mongo_controller.query(query_filter)

    # 刪除文檔
    # mongo_controller.delete(query_filter)

    # 關閉連接
    mongo_controller.close()
