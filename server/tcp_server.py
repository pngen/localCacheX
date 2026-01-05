import socket
import threading
from .protocol import RESPProtocol

class TCPServer:
    def __init__(self, cache, host='localhost', port=6379):
        self.cache = cache
        self.host = host
        self.port = port
        self.protocol = RESPProtocol(cache)
        self._running = False

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        self._running = True
        
        print(f"Starting TCP server on {self.host}:{self.port}")
        
        try:
            while self._running:
                client_socket, addr = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            server_socket.close()

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response = self.protocol.process_request(data)
                client_socket.send(response)
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()