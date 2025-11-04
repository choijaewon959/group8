import socket
import time
import threading
import random
import pandas as pd
from config import *


def get_price_data():
    # Simulate getting price data from a data source
    data = pd.read_csv('./data/market_data-1.csv')
    return data

def feed_price_stream():
    price_data = get_price_data()
    while True:
        print(price_data)
        time.sleep(1)  # Simulate a delay between price updates

def feed_news_stream():
    while True:
        sentiment = random.randint(0, 100)

def start_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen()
    print(f"Broadcast server running on {SERVER_HOST}:{SERVER_PORT}")

    # threads to handle different data streams
    threading.Thread(target=feed_price_stream, daemon=True).start()
    threading.Thread(target=feed_news_stream, daemon=True).start()

    while True:
        conn, addr = server.accept()
        data = conn.recv(BYTE_LIMIT)




if __name__ == "__main__":
    price_stream_thread = threading.Thread(target=start_price_stream)
    price_stream_thread.start()
