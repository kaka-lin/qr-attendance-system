import os
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)
from typing import List, Dict

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError
import pandas as pd

from config import config


class MongoController:
    def __init__(self, uri, db_name, collection_name):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print(f"Connected to database: {self.db_name}, collection: {self.collection_name}")
            self.collection.create_index([('中文姓名', 1), ('電子郵件地址', 1)], unique=True)
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")

    def create(self, data: Dict):
        try:
            result = self.collection.insert_one(data)
        except Exception as e:
            print(f"Failed to insert documents: {e}")
    
    def create_many(self, data: List[Dict]):        
        try:
            result = self.collection.insert_many(data, ordered=False)
        except Exception as e:
            print(f"Failed to insert multiple documents: {e}")

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

    def close(self):
        if self.client:
            self.client.close()
            print("Connection to MongoDB closed")


if __name__ == "__main__":
    # 初始化 MongoController，連接到 MongoDB Atlas 集群
    uri = config["MONGO_URI"]
    db_name = "test_database"
    collection_name = "test_collection"
    
    mongo_controller = MongoController(uri, db_name, collection_name)

    # 連接到 MongoDB 集群
    mongo_controller.connect()

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
