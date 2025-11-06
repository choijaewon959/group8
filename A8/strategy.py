import socket
from time import time
from multiprocessing import shared_memory
import numpy as np 
from orderbook import SharedPriceBook

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
def start_strategy(symbol):
    global tick_id
    global price_signals
    global news_signals

    # reset global variables as client starts 
    price_signals.clear()
    news_signals.clear()

    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(("localhost", 8999))
    client.sendall(b"REGISTER,STRATEGY,1*")
    counter = 0
    len_nums = 100
    
    # set shared news book object
    symbols = ['AAPL', 'SPY', 'MSFT']
    shared_price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book', create=False)
    shared_news_book = SharedNewsBook(symbols, name='G8_Shared_News_Book', create=False)
    
    # set strategy objects
    price_strategy = SimplePriceStrategy(symbol, shared_price_book, window=10)
    news_strategy = NewsSentimentStrategy(shared_news_book, symbol)


    while True: #counter < len_nums:
        res = client.recv(1024)
        if not res:
            break
        # print("[STRATEGY]", res.decode())
        output = res.decode().split('*')

        for msg in output:
            if not msg:
                continue

            fields = msg.split(',')
            tick_id += 1
            # meaningless : server tick id will not match with client side tick id unless they generated at same time. 
            # if int(fields[1]) != tick_id:
            #     print(f"[STRATEGY] Warning: Tick ID mismatch. Expected {tick_id}, got {fields[1]}")
            ts_sent = float(fields[-1])
            ts_rcvd = time()
            latency = ts_rcvd - ts_sent
            latency_logs.append(latency)

            # update news object
            if fields[0] == "NEWS":
                news_symbol = fields[2]
                sentiment = float(fields[3])
                shared_news_book.update(news_symbol, sentiment)

            # run the strategies : generate signals  
            price_signal = price_strategy.generate_signal()
            news_signal = news_strategy.generate_signal()
            
            if price_signal:
                print(f"[PRICE STRAT] {price_signal}")
                price_signals.append(price_signal)

            if news_signal:
                print(f"[NEWS STRAT] {news_signal}")
                news_signals.append(news_signal)

            counter += 1


        trade_time = time()
        decision_latency = trade_time - ts_sent
        print(f"[STRATEGY] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")
    # client.sendall(f"{total/counter}".encode())
    client.close()


if __name__ == "__main__":
    symbols = ['AAPL', 'SPY', 'MSFT']
    
    try:
        shared_price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book', create=True)
    except FileExistsError:
        shared_price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book', create=False)

    try:
        shared_news_book = SharedNewsBook(symbols, name='G8_Shared_News_Book', create=True)
    except FileExistsError:
        shared_news_book = SharedNewsBook(symbols, name='G8_Shared_News_Book', create=False)


    # run strategy
    start_strategy("AAPL")
