import socket
from time import time
from multiprocessing import shared_memory
import numpy as np 
from orderbook import SharedPriceBook
from config import *
import json
import threading
from shared_memory_utils import log_latency, log_memory_usage

# variables to calculate processing efficiency 
tick_id = 0
latency_logs = []
# saving the signals
price_signals = []
news_signals = []


# set news on shared memory
class SharedNewsBook:
    def __init__(self, symbols, name=None, create=True):
        self.symbols = symbols
        self.size = len(symbols)
        if create:
            self.shm = shared_memory.SharedMemory(create=True, size=self.size*8, name=name)
        else:
            self.shm = shared_memory.SharedMemory(name=name)
        
        self.sentiments = np.ndarray((self.size,), dtype=np.float64, buffer=self.shm.buf)
        self.symbol_index = {s: i for i, s in enumerate(symbols)}

    def update(self, symbol, sentiment):
        idx = self.symbol_index[symbol]
        self.sentiments[idx] = sentiment

    def read(self, symbol):
        idx = self.symbol_index[symbol]
        return self.sentiments[idx]



# set basic strategy classes 
class SimplePriceStrategy:
    def __init__(self, symbol: str, shared_price_book:SharedPriceBook, window: int = 10):
        self.symbol = symbol
        self.price_book = shared_price_book
        self.window = window
        self.price_history = [] 

    def update_price(self):
        # price from shared memory: price_book
        price = self.price_book.read(self.symbol)
        if price is None:
            return None
        self.price_history.append(price)
        if len(self.price_history) > self.window:
            self.price_history.pop(0)
        return price

    def generate_signal(self):
        # price from inner function 
        price = self.update_price()
        if price is None or len(self.price_history) < self.window:
            return None 
        ma = np.mean(self.price_history)
        print(ma)
        if price > ma:
            signal = "BUY"
            return {"symbol": self.symbol, "price": round(price, 2), "signal": signal}
        else:
            return None


# set basic strategy classes 
class NewsSentimentStrategy:
    def __init__(self, news_book:SharedNewsBook, symbol:str):
        self.news_book = news_book
        self.symbol = symbol

    def generate_signal(self):
        sentiment = self.news_book.read(self.symbol)
        if sentiment >= 50:
            return {"symbol": self.symbol, "sentiment": sentiment, "signal": "BUY"}
        return None


# total function ----------------------------------------------------------
# strategy.py
def start_price_strategy(symbol="AAPL"):
    global tick_id
    global price_signals
 
    # reset global variables as client starts 
    price_signals.clear()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8999))
    client.sendall(b"REGISTER,STRATEGY,1*")
    counter = 0
    len_nums = 100

    symbols = ['AAPL', 'SPY', 'MSFT']
    shared_price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book', create=False)
    price_strategy = SimplePriceStrategy(symbol, shared_price_book, window=10)

    while True: # counter < len_nums
        res = client.recv(1024)
        if not res:
            break
        output = res.decode().split('*')
        for msg in output:
            if not msg:
                continue

            fields = msg.split(',')
            tick_id += 1
            ts_sent = float(fields[-1])
            ts_rcvd = time()
            latency = ts_rcvd - ts_sent
            latency_logs.append(latency)

            price_signal = price_strategy.generate_signal()
            if price_signal:
                print(f"[PRICE STRAT] {price_signal}")
                price_signals.append(price_signal)
            
            counter += 1

        trade_time = time()
        decision_latency = trade_time - ts_sent
        
        # Log performance metrics to CSV
        log_latency("PRICE_STRATEGY", tick_id, latency, decision_latency, symbol)
        
        print(f"[PRICE STRATEGY] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")
        
        # Log memory usage every 50 ticks
        if tick_id % 50 == 0:
            log_memory_usage("PRICE_STRATEGY", 'G8_Shared_Prcie_Book')

    client.close()



def start_news_strategy(symbol="AAPL"):
    global tick_id
    global news_signals

    # reset global variables as client starts 
    news_signals.clear()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8999))
    client.sendall(b"REGISTER,STRATEGY,1*")
    counter = 0
    len_nums = 100

    symbols = ['AAPL', 'SPY', 'MSFT']
    shared_news_book = SharedNewsBook(symbols, name='G8_Shared_News_Book')
    news_strategy = NewsSentimentStrategy(shared_news_book, symbol)

    while True: # counter < len_nums:
        res = client.recv(1024)
        if not res:
            break
        output = res.decode().split('*')
        
        for msg in output:
            if not msg:
                continue
            fields = msg.split(',')
            tick_id +=1 
            ts_sent = float(fields[-1])
            ts_rcvd = time()
            latency = ts_rcvd - ts_sent
            latency_logs.append(latency)

            # update news object
            if fields[0] == "NEWS_SENTIMENT":
                news_symbol = fields[3]
                sentiment = float(fields[4])
                shared_news_book.update(news_symbol, sentiment)
            
            news_signal = news_strategy.generate_signal()
            
            if news_signal:
                #print(f"[NEWS STRAT] {news_signal}")
                news_signals.append(news_signal)

            counter += 1

        trade_time = time()
        decision_latency = trade_time - ts_sent
        
        # Log performance metrics to CSV
        log_latency("NEWS_STRATEGY", tick_id, latency, decision_latency, symbol)
        
        # Log memory usage every 50 ticks
        if tick_id % 50 == 0:
            log_memory_usage("NEWS_STRATEGY", 'G8_Shared_News_Book')
            
        #print(f"[NEWS STRATEGY] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")
    # client.sendall(f"{total/counter}".encode())
    client.close()


def send_price_order():
    global price_signals

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((MANAGER_HOST, MANAGER_PORT_GATEWAY))
    print("[PRICE STRATEGY] connected to OrderManager")

    while True:
        for price_signal in price_signals:
            client.sendall((json.dumps(price_signal) + "*").encode())
            print("[PRICE STRATEGY] sent price signal")

    client.close()

def send_news_order():
    global news_signals

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((MANAGER_HOST, MANAGER_PORT_GATEWAY))
    print("[NEWS STRATEGY] connected to OrderManager")

    while True:
        for news_signal in news_signals:
            client.sendall((json.dumps(news_signal) + "*").encode())
            print("[NEWS STRATEGY] sent price signal")

    client.close()


if __name__ == "__main__":
    """
    symbols = ['AAPL', 'SPY', 'MSFT']
    try:
        shared_price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book', create=True)
    except FileExistsError:
        shared_price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book', create=False)

    try:
        shared_news_book = SharedNewsBook(symbols, name='G8_Shared_News_Book', create=True)
    except FileExistsError:
        shared_news_book = SharedNewsBook(symbols, name='G8_Shared_News_Book', create=False)
    """
    #start_news_strategy()
    #start_price_strategy()

    t1 = threading.Thread(target=start_news_strategy, daemon=True)
    t2 = threading.Thread(target=start_price_strategy, daemon=True)

    t3 = threading.Thread(target=send_news_order, daemon=True)
    t4 = threading.Thread(target=send_price_order, daemon=True)

    t1.start()
    t2.start()

    t3.start()
    t4.start()

    t1.join()
    t2.join()

    t3.join()
    t4.join()

