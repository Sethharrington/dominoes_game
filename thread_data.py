import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *

currentId = "0"
# Positions for 4 players (corners of the screen)
pos = [
    (50, 50),      # Player 0 - Top Left
    (700, 50),     # Player 1 - Top Right
    (50, 500),     # Player 2 - Bottom Left
    (700, 500)     # Player 3 - Bottom Right
]


def thread_data(conn, curr_player):
    # conn.send(str.encode("Connected"))
    conn.send(str.encode(send_pos(pos[curr_player])))

    currentId = "1"
    reply = ''
    while True:
        try:
            data_str = conn.recv(2048).decode()
            
            if not data_str:
                print(f"Player {curr_player} disconnected")
                break
                
            data = read_pos(data_str)
            pos[curr_player] = data

            # Send all other players' positions (format: "x1,y1;x2,y2;x3,y3")
            other_positions = []
            for i in range(4):
                if i != curr_player:
                    other_positions.append(send_pos(pos[i]))
            
            reply = ";".join(other_positions)
            
            print(f"Player {curr_player} - Received: {data}, Sending: {reply}")

            conn.sendall(str.encode(reply))
        except Exception as e:
            print(f"Error with player {curr_player}: {e}")
            break

    print(f"Player {curr_player} connection closed")
    conn.close()
