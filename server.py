
"""Domino Game Server

Handles network communication for up to 4 players.
Each player connects and receives:
- Their starting position
- Real-time updates of other players' positions

The server maintains a shared state of all player positions
and broadcasts updates to keep all clients synchronized.
"""

import socket
from _thread import *
import sys
import os
from thread_data import *
from lib.utils import *

# Server Configuration
# Can be overridden with environment variables
server = os.environ.get("SERVER", 'localhost')
port = int(os.environ.get("PORT", 5558))

# Create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to address and port
try:
    s.bind((server, port))
    print(f"Server successfully bound to {server}:{port}")
except socket.error as e:
    print(f"ERROR: Could not bind server to {server}:{port}")
    print(f"Error: {e}")
    print("Make sure no other program is using this port")
    sys.exit(1)

# Listen for up to 4 connections (4 players max)
s.listen(4)
print("Waiting for connections (4 players needed)...")

# Accept connections and spawn threads
curr_player = 0
while True:
    conn, addr = s.accept()  # Block until a client connects
    
    if curr_player < 4:
        # Accept connection and assign player number
        print(f"Player {curr_player} connected from {addr}")
        start_new_thread(thread_data, (conn, curr_player))  # Handle player in separate thread
        curr_player += 1
        print(f"Players connected: {curr_player}/4")
    else:
        # Game is full, reject additional connections
        print(f"Game full! Rejecting connection from {addr}")
        conn.close()