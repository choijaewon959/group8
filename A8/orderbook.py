import socket
import time
from multiprocessing import shared_memory
import numpy as np
from shared_memory_utils import print_memory_usage, get_memory_footprint_mb, log_memory_usage, log_latency

# Variables for processing efficiency
tick_id = 0
latency_logs = []

class SharedPriceBook:
    def __init__(self, symbols, name=None, create=True):
        self.symbols = symbols  # List of stock symbols, e.g., ['AAPL', 'MSFT', 'SPY']
        self.size = len(symbols)  # Number of symbols

        if create:
            # Create shared memory for storing float prices for each symbol
            self.shm = shared_memory.SharedMemory(create=True, size=self.size*8, name=name)
        else:
            # Attach to existing shared memory
            self.shm = shared_memory.SharedMemory(name=name)

        # Create a numpy array backed by shared memory
        self.prices = np.ndarray((self.size,), dtype=np.float64, buffer=self.shm.buf)
        # Map each symbol to an index in the array
        self.symbol_index = {s: i for i, s in enumerate(symbols)}

    def update(self, symbol, price):
        idx = self.symbol_index[symbol]
        self.prices[idx] = price

    def read(self, symbol):
        idx = self.symbol_index[symbol]
        return self.prices[idx]


def start_orderbook():
    global tick_id

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 8999))
    client.sendall(b"REGISTER,ORDERBOOK,1*")  # Register as ORDERBOOK client

    symbols = ['AAPL', 'SPY', 'MSFT']
    
    # Create shared price book
    price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book')
    
    # Print initial memory usage
    print_memory_usage('G8_Shared_Prcie_Book', len(symbols))
    
    print(f"[ORDERBOOK] Started with symbols: {symbols}")

    while True:
        res = client.recv(1024)
        if not res:
            time.sleep(0.1)  # Wait and retry if no data received
            continue

        #print("[ORDERBOOK]", res.decode())
        output = res.decode().split('*')
        for msg in output:
            if not msg:
                continue

            fields = msg.split(',')
            tick_id += 1

            # fields[0] = MessageType: PRICE
            # fields[1] = tick_id
            # fields[2] = timestamp
            # fields[3] = symbol
            # fields[4] = price

            ts_sent = float(fields[-1])
            ts_rcvd = time.time()
            latency = ts_rcvd - ts_sent
            latency_logs.append(latency)

            symbol = fields[3]
            price = float(fields[4])
            price_book.update(symbol, price)

            print("Current order book status:", {s: price_book.read(s) for s in symbols})

        trade_time = time.time()
        decision_latency = trade_time - ts_sent
        #print(f"[ORDERBOOK] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")

        # Log performance metrics to CSV
        log_latency("ORDERBOOK", tick_id, latency, decision_latency, symbol)
        
        #print(f"[ORDERBOOK] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")
        
        # Print and log memory stats every 20 ticks
        if tick_id % 20 == 0:
            current_footprint = get_memory_footprint_mb('G8_Shared_Prcie_Book')
            #print(f"[MEMORY] Shared memory footprint: {current_footprint:.6f} MB")
            log_memory_usage("ORDERBOOK", 'G8_Shared_Prcie_Book')

    # Print final memory usage before closing
    #print("\n[ORDERBOOK] Shutting down...")
    print_memory_usage('G8_Shared_Prcie_Book', len(symbols))
    client.close()


if __name__ == "__main__":
    start_orderbook()
