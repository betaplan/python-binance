# config.py
import os

# 币安API配置
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

if not BINANCE_API_KEY or not BINANCE_API_SECRET:
    print("API Key 或 Secret 为空，请检查环境变量是否正确设置！")
else:
    print("API Key 获取成功！")
    
# MongoDB 配置
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = 'binance_futures'
COLLECTION_NAME = 'trade_data'

# 备份目录配置
BACKUP_DIR = os.getenv('BACKUP_DIR', 'backups/')
