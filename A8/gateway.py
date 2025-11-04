import socket
import time
import threading
import random
import pandas as pd
from config import *


# client servers
clients = {} # k: name, v: list

def get_price_data():
    # Simulate getting price data from a data source
    data = pd.read_csv('./data/market_data-1.csv')
    return data


def feed_price_stream():
    price_data = get_price_data()
    while True:
        # print(price_data)
        time.sleep(1)


def feed_news_stream():
    while True:
        sentiment = random.randint(0, 100)


def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")
    try:
        while True:
            time.sleep(1)
    except Exception:
        pass
    finally:
        print(f"[-] Disconnected: {addr}")
        clients.remove(conn)
        conn.close()


def start_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind((SERVER_HOST, SERVER_PORT_GATEWAY))
    server.listen()
    print(f"Broadcast server running on {SERVER_HOST}:{SERVER_PORT_GATEWAY}")

    # threads to handle different data streams
    threading.Thread(target=feed_price_stream, daemon=True).start()
    threading.Thread(target=feed_news_stream, daemon=True).start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
