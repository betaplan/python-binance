
# backup.py
import os
import json
from datetime import datetime
from database import Database
from config import BACKUP_DIR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import logging

from flask import Flask, jsonify, request

app = Flask(__name__)

db = Database()

@app.route('/api/trades', methods=['GET'])
def get_trades():
    symbol = request.args.get('symbol', 'BTCUSDT')
    limit = int(request.args.get('limit', 100))
    data = db.get_trade_data(query={'symbol': symbol}, limit=limit)
    return jsonify(data)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_backup(filename):
    filepath = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        # 将数据重新加载到数据库
        # 这里需要实现将数据批量插入到MongoDB的功能


def ensure_backup_dir_exists():
    """确保备份目录存在"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def backup_data():
    """备份内存中的交易数据到持久存储"""
    ensure_backup_dir_exists()
    data = db.get_trade_data()
    if data:
        filename = datetime.now().strftime('%Y%m%d') + '_backup.json'
        filepath = os.path.join(BACKUP_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f)
        print(f"数据备份成功，文件保存为 {filename}")
    else:
        print("没有交易数据需要备份。")



def list_backup_files():
    """列出备份目录中的所有备份文件"""
    files = [f for f in os.listdir(BACKUP_DIR) if f.endswith('_backup.json')]
    files.sort(reverse=True)  # 按照文件名降序排列，最新的备份文件排在最前面
    return files

def restore_data(filename=None):
    """从备份文件恢复交易数据到内存"""
    if filename is None:
        files = list_backup_files()
        if not files:
            print("没有可用的备份文件。")
            return
        print("可用的备份文件：")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")
        try:
            choice = int(input("请选择要恢复的备份文件编号："))
            if 1 <= choice <= len(files):
                filename = files[choice - 1]
            else:
                print("无效的选择。")
                return
        except ValueError:
            print("请输入有效的数字。")
            return

    filepath = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        if data:
            store_trade_data(data)
            print(f"数据恢复成功，已从 {filename} 加载 {len(data)} 条记录。")
        else:
            print(f"{filename} 中没有可用的数据。")
    else:
        print(f"备份文件 {filename} 不存在。")


def backup_job():
    """定时备份任务"""
    logger.info(f"开始执行数据备份任务：{datetime.now()}")
    backup_data()
    logger.info(f"数据备份任务完成：{datetime.now()}")

def start_scheduler():
    """启动定时任务调度器"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_job, 'interval', days=1, start_time='00:00:00')
    scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()
    logger.info("定时备份任务已启动。")

def job_listener(event):
    """监听定时任务执行结果"""
    if event.exception:
        logger.error(f"数据备份任务执行失败：{event}")
    else:
        logger.info(f"数据备份任务执行成功：{event}")
