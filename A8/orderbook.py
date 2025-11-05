import socket
import time

tick_id = 0
latency_logs = []

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
