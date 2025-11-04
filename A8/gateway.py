import socket
import time
import threading
import random
import pandas as pd
from collections import defaultdict
from config import *


# client servers
clients = defaultdict(list) # k: client type, v: list of client connections

def get_price_data():
    # Simulate getting price data from a data source
    data = pd.read_csv('./data/market_data-1.csv')
    return data


def get_sentiment_data():
    # Simulate news data from a data source
    data = pd.read_csv('./data/market_sentiment.csv')
    return data


def broadcast(msg: bytes, client_type: str):
    for conn in clients[client_type]:
        try:
            conn.sendall(msg)
        except Exception:
            print("[!] Dropping disconnected client.")
            clients.remove(conn)


def feed_price_stream():
    price_data = get_price_data()
    while True:
        for _, row in price_data.iterrows():
            price = row["price"]
            timestamp = row.get("timestamp", "")
            symbol = row["symbol"]

            # Create message
            message = f"{MessageType.PRICE.value},{timestamp},{symbol},{price},*".encode()
            
            # Broadcast to all strategy clients
            broadcast(message, ClientType.ORDERBOOK.value)
            
            # Simulate broadcast buffer
            time.sleep(1)


def feed_news_stream():
    news_data = get_sentiment_data()
    
    for _, row in news_data.iterrows():
        sentiment = int(row["sentiment"])
        timestamp = row.get("timestamp", "")
        symbol = row["symbol"]

        # Create message
        message = f"{MessageType.NEWS_SENTIMENT.value},{timestamp},{symbol},{sentiment},*".encode()
        
        # Broadcast to all strategy clients
        broadcast(message, ClientType.STRATEGY.value)
        
        # Simulate broadcast buffer
        time.sleep(1)


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

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_server()
