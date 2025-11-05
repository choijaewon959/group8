from multiprocessing import Process
from gateway import start_server
from orderbook import start_orderbook
from strategy import start_strategy

def run_gateway():
    print("[Gateway] Starting feed server...")
    start_server()

def run_orderbook():
    print("[ORDERBOOK] Starting orderbook client...")
    start_orderbook()

def run_strategy():
    print("[STRATEGY] Starting strategy client...")
    start_strategy()




if __name__ == "__main__":
    processes = [
        Process(target=run_gateway),
        Process(target=run_orderbook),
        Process(target=run_strategy),
        # Process(target=run_ordermanager)
    ]
    for p in processes: p.start()
    for p in processes: p.join()