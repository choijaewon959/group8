from multiprocessing import Process
from time import sleep
from gateway import start_server
from orderbook import start_orderbook
from order_manager import start_ordermanager
from strategy import start_news_strategy, start_price_strategy

def run_gateway():
    print("[Gateway] Starting feed server...")
    start_server()

def run_orderbook():
    sleep(1)
    print("[ORDERBOOK] Starting orderbook client...")
    start_orderbook()

def run_price_strategy():
    sleep(2)
    print("[STRATEGY] Starting price strategy...")
    start_price_strategy()

def run_news_strategy():
    sleep(2)
    print("[STRATEGY] Starting news strategy...")
    start_news_strategy()

def run_ordermanager():
    sleep(3)
    print("[ORDER MANAGER] Starting order manager...")
    start_ordermanager()


if __name__ == "__main__":
    processes = [
        Process(target=run_gateway),
        Process(target=run_orderbook),
        Process(target=run_price_strategy),
        Process(target=run_news_strategy),        
        Process(target=run_ordermanager)
    ]
    for p in processes: p.start()
    for p in processes: p.join()
