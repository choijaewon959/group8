import socket
import threading
import json
from datetime import datetime
from config import *
from collections import defaultdict

from psutil._common import addr


clients = defaultdict()

"""
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
"""


def log_trade(order: dict):
    #Deserialize each order and log the trade
    qty = order['qty']
    price = order['price']
    side = order['side']
    timestamp = order['timestamp']
    order_id = order['order_id']

    confirmation = print(f"[RECEIVED ORDER FROM {addr}: [ORDER ID:{order_id}] {qty} {side} signal at {price}")

    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp}, {confirmation}\n")


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
            print("buffer:", buffer)

            #data.decode('utf-8'))
            #order = json.loads(buffer)
            #log_trade(order)
            print('buffer: ', buffer)

            while MESSAGE_DELIMITER in buffer:
                # split the message from the buffer, process a message a time
                msg, buffer = buffer.split(MESSAGE_DELIMITER, 1)
                msg_decoded = msg.decode("utf-8")
                #order = json.loads(buffer)
                #log_trade(order)
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


def start_ordermanager():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )
    server.bind((SERVER_HOST_OM, SERVER_PORT_GATEWAY_OM))
    server.listen()
    print(f"[ORDER MANAGER] Broadcasting on {SERVER_HOST_OM}:{SERVER_PORT_GATEWAY_OM}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    start_ordermanager()


