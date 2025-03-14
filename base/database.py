
# database.py
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

class Database:
    def __init__(self, uri=MONGO_URI, db_name=DATABASE_NAME, collection_name=COLLECTION_NAME):
        """
        初始化数据库连接。
        :param uri: MongoDB 连接 URI。
        :param db_name: 数据库名称。
        :param collection_name: 集合名称。
        """
        try:
            self.client = MongoClient(uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
            print(f"成功连接到数据库：{db_name}，集合：{collection_name}")
        except ConnectionFailure as e:
            print(f"Connection failed: {e}")
            raise
        except Exception as e:
            print(f"初始化数据库时发生错误：{e}")
            raise

    def store_trade_data(self, data):
        """
        将交易数据存储到数据库中。
        :param data: 交易数据列表，每个元素是一个字典。
        """
        if data:
            try:
                self.collection.insert_many(data, ordered=False)
                print(f"成功插入 {len(data)} 条数据。")
            except OperationFailure as e:
                print(f"数据插入失败：{e}")
            except Exception as e:
                print(f"存储数据时发生错误：{e}")
        else:
            print("没有数据需要存储。")

    def get_trade_data(self, query=None, limit=100):
        """
        查询交易数据。
        :param query: 查询条件，默认为 None，表示获取所有数据。
        :param limit: 返回的最大记录数，默认为 100。
        :return: 交易数据列表。
        """
        if query is None:
            query = {}
        try:
            cursor = self.collection.find(query).limit(limit)
            data = list(cursor)
            print(f"成功查询到 {len(data)} 条数据。")
            return data
        except OperationFailure as e:
            print(f"数据查询失败：{e}")
        except Exception as e:
            print(f"查询数据时发生错误：{e}")
        return []

    def create_index(self, field_name, ascending=True):
        """
        创建索引以提高查询性能。
        :param field_name: 索引字段名称。
        :param ascending: 是否创建升序索引，默认为 True（升序），False 为降序。
        """
        try:
            direction = ASCENDING if ascending else DESCENDING
            self.collection.create_index([(field_name, direction)])
            print(f"成功在字段 '{field_name}' 上创建 {'升序' if ascending else '降序'} 索引。")
        except OperationFailure as e:
            print(f"创建索引失败：{e}")
        except Exception as e:
            print(f"创建索引时发生错误：{e}")

    def close(self):
        """
        关闭数据库连接。
        """
        try:
            self.client.close()
            print("数据库连接已关闭。")
        except Exception as e:
            print(f"关闭数据库连接时发生错误：{e}")