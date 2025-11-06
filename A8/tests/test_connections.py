import socket
import threading
import time

def test_server_socket_creation():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('localhost', 9000))
        server_socket.listen(5)
        bound_successfully = True
    except OSError:
        bound_successfully = False
    finally:
        server_socket.close()
    
    assert bound_successfully

def test_client_connection_to_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 9001))
    server_socket.listen(1)
    
    connections = []
    
    def accept_connection():
        try:
            conn, addr = server_socket.accept()
            connections.append((conn, addr))
        except:
            pass
    
    accept_thread = threading.Thread(target=accept_connection)
    accept_thread.daemon = True
    accept_thread.start()
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2.0)
    
    try:
        client_socket.connect(('localhost', 9001))
        connection_successful = True
    except:
        connection_successful = False
    finally:
        client_socket.close()
    
    accept_thread.join(timeout=1.0)
    
    if connections:
        connections[0][0].close()
    server_socket.close()

    assert connection_successful
    assert len(connections) > 0