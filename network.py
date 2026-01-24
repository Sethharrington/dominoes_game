"""Network Client

Handles client-side network communication with the game server.
Manages connection, sending player data, and receiving game state updates.
"""

import socket
import os

class Network():
    """Network communication handler for game client"""
    
    def __init__(self):
        """Initialize network connection to server"""
        # Create TCP socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Server configuration (can be overridden with env variables)
        self.server = os.environ.get("SERVER", 'localhost')
        self.port = int(os.environ.get("PORT", 5558))
        self.addr = (self.server, self.port)
        
        # Connect and get initial position from server
        self.pos = self.connect()

    def get_pos(self):
        """Get the initial position received from server
        
        Returns:
            str: Position string in format "x,y"
        """
        return self.pos

    def connect(self):
        """Establish connection to game server
        
        Returns:
            str: Initial position data from server, or None if connection fails
        """
        print(f"Attempting to connect to {self.addr}")
        try:
            self.client.connect(self.addr)
            # Receive initial position assignment from server
            data = self.client.recv(2048).decode()
            print(f"Connected successfully! Received: {data}")
            return data
        except Exception as e:
            print(f"Connection failed: {e}")
            return None
        
    def send(self, data):
        """Send data to server and receive response
        
        Args:
            data: String data to send (typically player position)
            
        Returns:
            str: Server response (other players' positions)
            
        Raises:
            socket.error: If connection is lost
        """
        try:
            # Send player data to server
            self.client.send(str.encode(data))
            # Receive and return server response
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Network error: {e}")
            raise  # Re-raise to let game.py handle disconnection