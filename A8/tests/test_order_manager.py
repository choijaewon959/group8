import socket
import threading
import time
import json
from group8.A8.config import *


def test_manager_receiving_correct_number_of_orders():

    trades_received = []

    def handle_client(conn, args):
        buffer = b""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            buffer += data

            while MESSAGE_DELIMITER in buffer:
                msg, buffer = buffer.split(MESSAGE_DELIMITER, 1)
                order = json.loads(msg.decode())
                trades_received.append(order)

    def run_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', 9002))
        server.listen()

        conn, addr = server.accept()
        handle_client(conn, addr)
        server.close()

    mock_manager = threading.Thread(target=run_server, daemon=True)
    mock_manager.start()

    time.sleep(1)

    mock_orders = [{'symbol':'AAPL','price':100,'signal':'BUY'},
                   {'symbol':'AAPL','price':105,'signal':'BUY'},
                   {'symbol':'AAPL','price':110,'signal':'BUY'}]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 9002))
    for order in mock_orders:
        client.sendall(json.dumps(order).encode() + MESSAGE_DELIMITER)
    client.close()

    time.sleep(1)

    assert len(trades_received) == len(mock_orders)

    for msg_sent, msg_received in zip(mock_orders, trades_received):
        assert msg_sent == msg_received

    MOCK_LOG_FILE = "mocktrade.log"

    for trade in trades_received:
        confirmation = f"[RECEIVED ORDER]: {1} {trade["symbol"]} {trade["price"]} signal at {trade["signal"]}"

        with open(MOCK_LOG_FILE, 'a') as f:
            f.write(confirmation + "\n")

    with open(MOCK_LOG_FILE) as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(mock_orders)

    for line, order in zip(lines, mock_orders):

        assert order['symbol'] in line
        assert str(order['price']) in line
        assert order['signal'] in line







