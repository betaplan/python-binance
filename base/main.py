# main.py
from database import Database

# 初始化数据库连接
db = Database()

# 创建索引（例如在 'time' 字段上创建升序索引）
db.create_index('time', ascending=True)

# 存储数据
sample_data = [
    {'symbol': 'BTCUSDT', 'price': 45000.0, 'qty': 0.1, 'time': 1617184800000, 'is_buyer_market_maker': False},
    # 更多数据...
]
db.store_trade_data(sample_data)

# 查询数据
data = db.get_trade_data(query={'symbol': 'BTCUSDT'}, limit=10)
for record in data:
    print(record)

# 关闭数据库连接
db.close()


from backup import start_scheduler

if __name__ == '__main__':
    start_scheduler()
    # 其他初始化代码