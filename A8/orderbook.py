import socket

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect(("localhost", 8999))
client.sendall(b"REGISTER,STRATEGY,1*")
counter = 0
len_nums = 100
total = 0

while counter < len_nums:
    res = client.recv(1024)
    if not res:
        break
    
    print(res.decode())
    
# client.sendall(f"{total/counter}".encode())
client.close()

