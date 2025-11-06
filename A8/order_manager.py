import socket
import threading
import json
from datetime import datetime

from psutil._common import addr


class OrderManager():

    def __init__(self, host='localhost', port=8000, log_file="trades.log"):
        self.host = host
        self.port = port
        self.log_file = log_file
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_STREAM
                                           )
        self.server_socket.setsockopt(socket.SOL_SOCKET,
                               socket.SO_REUSEADDR,
                               1
                               )
        self.running = False

    def handle_client(self, conn, addr):
        #handle strategy objects coming from strategy clients
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                try:
                    buffer = data.decode('utf-8')
                    order = json.loads(buffer)
                    self.log_trade(order)
                except Exception as e:
                    print(f"[ERROR] {e} Failing to process order from {addr}")


    def log_trade(self, order: dict):
        #Deserialize each order and log the trade
        self.qty = order['qty']
        self.price = order['price']
        self.side = order['side']
        self.timestamp = order['timestamp']
        self.order_id = order['order_id']

        confirmation = print(f"[RECEIVED ORDER FROM {addr}: [ORDER ID:{self.order_id}] {self.qty} {self.side} signal at {self.price}")

        with open(self.log_file, 'a') as f:
            f.write(f"{self.timestamp}, {confirmation}\n")


def start_orderbook():
    global tick_id

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect(("localhost", 8999))
    client.sendall(b"REGISTER,ORDERBOOK,1*")
    counter = 0
    len_nums = 100
    total = 0

    # set Orderbook object on Shared Memory
    symbols = ['AAPL', 'SPY', 'MSFT']
    price_book = SharedPriceBook(symbols, name='G8_Shared_Prcie_Book')

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

            # meaningless : server tick id will not match with client side tick id unless they generated at same time.
            # if int(fields[1]) != tick_id:
            #     print(f"[ORDERBOOK] Warning: Tick ID mismatch. Expected {tick_id}, got {fields[1]}")

            ts_sent = float(fields[-1])
            ts_rcvd = time.time()
            latency = ts_rcvd - ts_sent
            latency_logs.append(latency)

            # update orderbook
            symbol = fields[2]
            price = float(fields[3])
            price_book.update(symbol, price)

        trade_time = time.time()
        decision_latency = trade_time - ts_sent
        print(f"[ORDERBOOK] Latency: {latency:.6f} seconds, Decision Latency: {decision_latency:.6f} seconds")

        # print(res.decode())

    # client.sendall(f"{total/counter}".encode())
    client.close()

def start_ordermanager(self):
    #start the order manager server
    self.server_socket.bind((
        self.host,
        self.port)
    )

    self.server_socket.listen()
    self.running = True
    print(f"[ORDER MANAGER] Broadcasting on {self.host}:{self.port}...")

    try:
        while self.running:
            conn, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client(), args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("[ORDER MANAGER] Shutting down")
    finally:
        self.server_socket.close()

if __name__ == "__main__":
    start_ordermanager()

"""
order = OrderManager()
order.start()
order.handle_client(order.host, order.port)
"""


