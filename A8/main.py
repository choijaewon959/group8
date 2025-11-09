from multiprocessing import Process
from time import sleep
import signal
import sys
from gateway import start_server
from orderbook import start_orderbook
from order_manager import start_ordermanager
from strategy import start_news_strategy, start_price_strategy, send_price_order, send_news_order
from shared_memory_utils import print_memory_usage

def signal_handler():
    print('\n[MAIN] Shutting down...')
    print_memory_usage('G8_Shared_Prcie_Book')
    print('[MAIN] Performance logs saved to logs/ directory')
    sys.exit(0)

def run_gateway():
    print("[Gateway] Starting feed server...")
    start_server()

def run_orderbook():
    sleep(1)
    print("[ORDERBOOK] Starting orderbook client...")
    start_orderbook()

def run_ordermanager():
    print("[ORDER MANAGER] Starting order manager...")
    start_ordermanager()

def run_price_strategy():
    sleep(2)
    print("[STRATEGY] Starting price strategy...")
    start_price_strategy()

def run_news_strategy():
    sleep(2)
    print("[STRATEGY] Starting news strategy...")
    start_news_strategy()


if __name__ == "__main__":
    # Handle Ctrl+C gracefully with memory report
    signal.signal(signal.SIGINT, signal_handler)
    
    print("[MAIN] Starting A8 Trading System with Performance Logging...")
    print("[MAIN] Performance data will be logged to CSV files in logs/ directory")
    
    processes = [
        Process(target=run_gateway),
        Process(target=run_orderbook),
        Process(target=run_ordermanager),
        Process(target=run_price_strategy),
        Process(target=run_news_strategy),
    ]
    
    for p in processes: p.start()
    
    try:
        for p in processes: p.join()
    except KeyboardInterrupt:
        print('\n[MAIN] Terminating processes...')
        for p in processes:
            p.terminate()
        print('[MAIN] Performance logs saved to logs/ directory')
        print('[MAIN] All processes terminated')
