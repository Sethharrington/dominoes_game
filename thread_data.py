"""Thread Data Handler

Manages individual player connections in separate threads.
Each player thread:
1. Sends initial position to client
2. Receives player position updates
3. Broadcasts other players' positions back
4. Handles disconnections gracefully
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.utils import *

currentId = "0"

# Shared game state - positions for all 4 players
# These are starting positions at the corners of the screen
pos = [
    (50, 50),      # Player 0 - Top Left corner
    (700, 50),     # Player 1 - Top Right corner
    (50, 500),     # Player 2 - Bottom Left corner
    (700, 500)     # Player 3 - Bottom Right corner
]


def thread_data(conn, curr_player):
    """Handle communication for a single player connection
    
    Args:
        conn: socket connection object
        curr_player: player number (0-3)
    """
    
    # Send initial position to the connecting player
    conn.send(str.encode(send_pos(pos[curr_player])))

    currentId = "1"
    reply = ''
    
    # Main communication loop
    while True:
        try:
            # Receive updated position from this player
            data_str = conn.recv(2048).decode()
            
            # Check for disconnection
            if not data_str:
                print(f"Player {curr_player} disconnected")
                break
            
            # Parse and update this player's position in shared state
            data = read_pos(data_str)
            pos[curr_player] = data

            # Build response containing all OTHER players' positions
            # Format: "x1,y1;x2,y2;x3,y3" (semicolon-separated)
            other_positions = []
            for i in range(4):
                if i != curr_player:  # Exclude this player
                    other_positions.append(send_pos(pos[i]))
            
            reply = ";".join(other_positions)
            
            # Debug output
            print(f"Player {curr_player} - Received: {data}, Sending: {reply}")

            # Send other players' positions back to this player
            conn.sendall(str.encode(reply))
            
        except Exception as e:
            print(f"Error with player {curr_player}: {e}")
            break

    # Cleanup when player disconnects
    print(f"Player {curr_player} connection closed")
    conn.close()
