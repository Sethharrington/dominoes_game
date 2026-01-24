"""Domino Game - Multiplayer Client

This is a 4-player networked domino game where each player can:
- See their own domino tiles
- Drag and drop tiles
- Rotate tiles with the F key
- See other players' positions (but not their tiles)
"""

import pygame
import sys
from classes.domino_game import *

# Window creation - Get screen size and create a resizable window
x, y = pygame.display.set_mode().get_size()
win = pygame.display.set_mode((x/2,y/2), pygame.RESIZABLE)
pygame.display.set_caption("Domino Game")

clientNumber = 0

# Import game modules
from network import *
from classes.domino_game import Domino_Game
from classes.player import *
from lib.utils import *

def redrawWindow(win, players):
    """Redraw the game window with all players and their tiles
    
    Args:
        win: pygame display surface
        players: list of Player objects to draw
    """
    win.fill((255,255,255))  # Clear screen with white
    for player in players:
        player.draw_tiles_hand(win)
    pygame.display.update()

def main():
    """Main game loop - handles network connection, game setup, and event processing"""
    
    # Create the domino game manager
    dg = Domino_Game()
    run = True
    
    # Network Setup - Connect to server
    try:
        n = Network()
        startPos = read_pos(n.get_pos())  # Get starting position from server
        print(f"Connected! Starting at position: {startPos}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        print("Make sure the server is running.")
        return
    
    # Create 4 players with different colors
    # p1 is THIS client's player, others represent remote players
    p1 = Player(startPos[0], startPos[1], 60, 120, (0, 255, 0))     # Green - This player
    p2 = Player(50, 50, 60, 120, (255, 0, 0))                       # Red - Remote player 1
    p3 = Player(50, 50, 60, 120, (0, 0, 255))                       # Blue - Remote player 2
    p4 = Player(50, 50, 60, 120, (255, 255, 0))                     # Yellow - Remote player 3
    other_players = [p2, p3, p4]
    
    # Deal domino tiles - only for this player (p1)
    # Other players' hands are kept private on their own clients
    p1.set_tiles_hand(dg.get_tiles_hand())
    
    # Game clock for frame rate control
    clock = pygame.time.Clock()

    # Main game loop
    while run:
        clock.tick(60)  # Limit to 60 FPS
        
        # Network Synchronization
        try:
            # Send this player's position to server
            # Receive all other players' positions as response
            response = n.send(send_pos((p1.x, p1.y)))
            other_positions = read_all_players(response)  # Parse "x1,y1;x2,y2;x3,y3" format
            
            # Update other players' positions with data from server
            for i, player in enumerate(other_players):
                if i < len(other_positions):
                    player.x = other_positions[i][0]
                    player.y = other_positions[i][1]
                    player.update()
                    
        except Exception as e:
            print(f"Connection lost: {e}")
            run = False
            break

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            # Mouse Click - Pick up or drop tiles
            if event.type == pygame.MOUSEBUTTONDOWN:
                carrying_something = False
                
                # Check if any tile is being carried
                for sprite in p1.tiles_group:
                    if sprite.is_carried:
                        sprite.is_carried = False  # Drop the tile
                        carrying_something = True
                        
                # If not carrying anything, check if clicking on a tile to pick it up
                if not carrying_something:
                    for sprite in reversed(p1.tiles_group.sprites()):
                        if sprite.check_click(event.pos):
                            break  # Stop after picking up one tile
                            
            # Keyboard - F key to rotate carried tile
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Rotate any tile currently being carried
                    for sprite in p1.tiles_group:
                        if sprite.is_carried:
                            sprite.rotate()

        # Update player movement (arrow keys)
        p1.move()

        # Update tile positions (follows mouse if carried)
        p1.tiles_group.update()

        # Render everything
        win.fill((255, 255, 255))  # Clear screen
        for player in [p1, p2, p3, p4]:
            player.draw_tiles_hand(win)
        pygame.display.update()

main()