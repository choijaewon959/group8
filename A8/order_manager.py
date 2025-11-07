import socket
import threading
import json
from config import *

def log_trade(order: dict, addr, message_type:str):
    #Deserialize each order and log the trade
    if message_type == MessageType.NEWS_SENTIMENT.value:
        value = order['sentiment']
    elif message_type == MessageType.PRICE.value:
        value = order['price']

    symbol = order['symbol']
    signal = order['signal']

    confirmation = f"[RECEIVED ORDER FROM {addr}]: {1} {symbol} {signal} signal at {value}"
    print(confirmation)

    with open(LOG_FILE, 'a') as f:
        f.write(confirmation + "\n")


def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")
    buffer = b""

    try:
        while True:
            data = conn.recv(BYTE_LIMIT)
            if not data:
                break
            buffer += data
            print("buffer:", buffer)

            while MESSAGE_DELIMITER in buffer:
                # split the message from the buffer, process a message a time
                msg, buffer = buffer.split(MESSAGE_DELIMITER, 1)
                order = json.loads(msg.decode())
                log_trade(order, addr, MessageType.NEWS_SENTIMENT.value if "sentiment" in order.keys() else MessageType.PRICE.value)

    except Exception as e:
        print(f"[!] Connection error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Disconnected {addr}")


def start_ordermanager():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind((MANAGER_HOST, MANAGER_PORT_GATEWAY))
    server.listen()
    print(f"[ORDER MANAGER] Broadcasting on {MANAGER_HOST}:{MANAGER_PORT_GATEWAY}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_ordermanager()


