import socket
import os

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = os.environ.get("SERVER", 'localhost')
        self.port = int(os.environ.get("PORT", 5558))
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def get_pos(self):
        return self.pos

    def connect(self):
        print(f"Attempting to connect to {self.addr}")
        try:
            self.client.connect(self.addr)
            data = self.client.recv(2048).decode()
            print(f"Connected successfully! Received: {data}")
            return data
        except Exception as e:
            print(f"Connection failed: {e}")
            return None
        
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Network error: {e}")
            raise  # Re-raise to let game.py handle it