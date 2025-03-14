# api.py
from flask import Flask, jsonify, request
from database import Database
from backup import list_backup_files, restore_data

app = Flask(__name__)

# 初始化数据库连接
db = Database()

@app.route('/')
def home():
    return "Welcome to my API!"

# 获取交易数据
@app.route('/api/trades', methods=['GET'])
def get_trades():
    symbol = request.args.get('symbol', 'BTCUSDT')
    limit = int(request.args.get('limit', 100))
    data = db.get_trade_data(query={'symbol': symbol}, limit=limit)
    return jsonify(data)

# 获取备份文件列表
@app.route('/api/backups', methods=['GET'])
def get_backups():
    files = list_backup_files()
    return jsonify(files)

# 恢复数据
@app.route('/api/restore', methods=['POST'])
def restore_data():
    filename = request.json.get('filename')
    if filename:
        restore_data(filename)
        return jsonify({"message": "数据恢复成功"}), 200
    else:
        return jsonify({"error": "缺少备份文件名"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)