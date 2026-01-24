
import socket
from _thread import *
import sys
import os
from thread_data import *
from lib.utils import *

server = os.environ.get("SERVER", 'localhost')
port = int(os.environ.get("PORT", 5558))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
    print(f"Server successfully bound to {server}:{port}")
except socket.error as e:
    print(f"ERROR: Could not bind server to {server}:{port}")
    print(f"Error: {e}")
    print("Make sure no other program is using this port")
    sys.exit(1)

s.listen(4)
print("Waiting for connections (4 players needed)...")

curr_player = 0
while True:
    conn, addr = s.accept()
    
    if curr_player < 4:
        print(f"Player {curr_player} connected from {addr}")
        start_new_thread(thread_data, (conn, curr_player))
        curr_player += 1
        print(f"Players connected: {curr_player}/4")
    else:
        print(f"Game full! Rejecting connection from {addr}")
        conn.close()