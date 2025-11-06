import socket
import time
from multiprocessing import shared_memory
import numpy as np 

tick_id = 0
latency_logs = []


class SharedPriceBook: 
    def __init__(self, symbols, name=None):
        self.symbols = symbols # list of symbols : ['AAPL', 'MSFT'. 'SPY']
        self.size = len(symbols) # number of symbols : 3 
        self.shm = shared_memory.SharedMemory(create=True, size=self.size*8, name=name)
        self.prices = np.ndarray((self.size,), dtype=np.float64, buffer=self.shm.buf)
        self.symbol_index = {s: i for i, s in enumerate(symbols)}
    
    def update(self, symbol, price):
        idx = self.symbol_index[symbol]
        self.prices[idx] = price

    def read(self, symbol):
        idx = self.symbol_index[symbol]
        return self.prices[idx]



def start_orderbook():
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect(("localhost", 8999))
    client.sendall(b"REGISTER,ORDERBOOK,1*")
    counter = 0
    len_nums = 100
    total = 0

    while counter < len_nums:
        res = client.recv(1024)
        if not res:
            break
        print("[ORDERBOOK]", res.decode())
        output = res.decode().split('*')
        for msg in output:
            if msg == '':
                continue
            fields = msg.split(',')
            tick_id += 1
            if int(fields[1]) != tick_id:
                print(f"[ORDERBOOK] Warning: Tick ID mismatch. Expected {tick_id}, got {fields[1]}")
            ts_sent = float(fields[-1])
            ts_rcvd = time.time()
            latency = ts_rcvd - ts_sent
            latency_logs.append(latency)

        '''
            @TODO: Add trade decision here
        '''
        trade_time = time.time()
        decision_latency = trade_time - ts_sent
        print(f"[ORDERBOOK] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")

        # print(res.decode())
        
    # client.sendall(f"{total/counter}".encode())
    client.close()


if __name__ == "__main__":
    start_orderbook()
