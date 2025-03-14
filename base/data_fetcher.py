# data_fetcher.py
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from config import BINANCE_API_KEY, BINANCE_API_SECRET
from database import Database
import requests

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 初始化数据库连接
db = Database()

# 初始化币安客户端
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def fetch_trade_data_requests(symbol='BTCUSDT'):
    url = f'https://api.binance.com/api/v3/trades'
    params = {
        'symbol': symbol,
        'limit': 1000
    }
    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # 错误处理
        return []
    


def fetch_trade_data(symbol='BTCUSDT', limit=1000):
    """
    从币安获取指定交易对的逐笔交易数据。

    参数:
        symbol (str): 交易对，例如 'BTCUSDT'。
        limit (int): 获取的交易记录数量，最大值为 1000。

    返回:
        list: 交易数据列表，每个元素是一个字典，包含交易信息。
    """
    try:
        # 获取交易数据
        trades = client.get_recent_trades(symbol=symbol, limit=limit)
        logger.info(f"成功获取 {len(trades)} 条 {symbol} 的交易数据。")
        return trades
    except BinanceAPIException as e:
        logger.error(f"Binance API 错误: {e}")
    except BinanceRequestException as e:
        logger.error(f"Binance 请求错误: {e}")
    except Exception as e:
        logger.error(f"获取交易数据时发生错误: {e}")
    return []

def process_and_store_data(symbol='BTCUSDT', limit=1000):
    """
    获取交易数据并处理后存储到数据库。

    参数:
        symbol (str): 交易对，例如 'BTCUSDT'。
        limit (int): 获取的交易记录数量，最大值为 1000。
    """
    # 获取交易数据
    trades = fetch_trade_data(symbol, limit)
    if trades:
        # 处理数据（根据需要进行数据清洗、转换等操作）
        processed_data = []
        for trade in trades:
            processed_data.append({
                'symbol': trade['symbol'],
                'price': float(trade['price']),
                'qty': float(trade['qty']),
                'time': trade['time'],
                'is_buyer_market_maker': trade['isBuyerMaker']
            })
        # 存储数据到数据库
        db.store_trade_data(processed_data)
    else:
        logger.warning(f"未获取到 {symbol} 的交易数据，跳过存储。")