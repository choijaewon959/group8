import socket
import time
import threading
import pandas as pd
from collections import defaultdict
from config import *


# client servers
clients = defaultdict(list) # k: client type, v: list of client connections

# Shared global counters
price_tick_count = 0
news_tick_count = 0

# Previous counts for throughput calculation
prev_price = 0
prev_news = 0

# price and news tick ids
price_tick_id = 0
news_tick_id = 0

# Thread lock for synchronizing access to shared resources
lock = threading.Lock()






# monitoring throughput
def monitor_throughput(interval=5):
    global price_tick_count, news_tick_count, prev_price, prev_news
    while True:
        time.sleep(interval)
        with lock:
            delta_price = price_tick_count - prev_price
            delta_news = news_tick_count - prev_news
            prev_price = price_tick_count
            prev_news = news_tick_count

        rate_price = delta_price / interval
        rate_news = delta_news / interval
        print(f"[THROUGHPUT] Price ticks/sec: {rate_price}, News ticks/sec: {rate_news}")


def get_price_data():
    # Simulate getting price data from a data source
    data = pd.read_csv('./data/market_data-1.csv')
    return data


def get_sentiment_data():
    # Simulate news data from a data source
    data = pd.read_csv('./data/market_sentiment.csv')
    return data


def broadcast(msg: bytes, client_type: str):
    global price_tick_count, news_tick_count
    if client_type == ClientType.ORDERBOOK.value:
        with lock:
            price_tick_count += 1
    elif client_type == ClientType.STRATEGY.value:
        with lock:
            news_tick_count += 1

    for conn in clients[client_type]:
        try:
            conn.sendall(msg)
        except Exception:
            print("[!] Dropping disconnected client.")
            clients.pop(client_type, None)


def feed_price_stream():
    global price_tick_count
    price_data = get_price_data()
    
    for _, row in price_data.iterrows():
        price = row["price"]
        timestamp = row.get("timestamp", "")
        symbol = row["symbol"]
        feed_time = time.time()
        price_tick_count += 1

        # Create message
        message = f"{MessageType.PRICE.value},{price_tick_count},{timestamp},{symbol},{price},{feed_time}*".encode()

        # wait for a short interval to simulate real-time feed
        time.sleep(0.01)

        # Broadcast to all strategy clients
        broadcast(message, ClientType.ORDERBOOK.value)


def feed_news_stream():
    global news_tick_count
    news_data = get_sentiment_data()
    
    for _, row in news_data.iterrows():
        sentiment = int(row["sentiment"])
        timestamp = row.get("timestamp", "")
        symbol = row["symbol"]
        feed_time = time.time()
        news_tick_count += 1

        # Create message
        message = f"{MessageType.NEWS_SENTIMENT.value},{news_tick_count},{timestamp},{symbol},{sentiment},{feed_time}*".encode()

        # wait for a short interval to simulate real-time feed
        time.sleep(0.01)

        # Broadcast to all strategy clients
        broadcast(message, ClientType.STRATEGY.value)


def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")
    buffer = b""
    client_type = None

    try:
        while True:
            data = conn.recv(BYTE_LIMIT)
            if not data:
                break
            buffer += data
            print('buffer: ', buffer)

            while MESSAGE_DELIMITER in buffer:
                # split the message from the buffer, process a message a time
                msg, buffer = buffer.split(MESSAGE_DELIMITER, 1)
                msg_decoded = msg.decode()
                msg_type, client_type, client_id = msg_decoded.split(STRING_DELIMITER)

                if msg_type == MessageType.REGISTER.value:
                    clients[client_type].append(conn)
                    print(f"[+] Registered client: {client_type}: {client_id}")
    except Exception as e:
        print(f"[!] Connection error with {addr}: {e}")
    finally:
        if client_type and client_type in clients:
            del clients[client_type]
        conn.close()
        print(f"[-] Disconnected {addr}")
                    

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

    # thread to monitor throughput
    threading.Thread(target=monitor_throughput, daemon=True).start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
