import pygame
import sys
from classes.domino_game import *

# Window creation
x, y = pygame.display.set_mode().get_size()
win = pygame.display.set_mode((x/2,y/2), pygame.RESIZABLE)
pygame.display.set_caption("Domino Game")

clientNumber = 0
# Add project root to path

from network import *
from classes.domino_game import Domino_Game
from classes.player import *
from lib.utils import *

def redrawWindow(win, players):
    win.fill((255,255,255))
    for player in players:
        player.draw_tiles_hand(win)
    pygame.display.update()

def main():
    dg = Domino_Game()
    run = True
    # Sockets
    try:
        n = Network()
        startPos = read_pos(n.get_pos())
        print(f"Connected! Starting at position: {startPos}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        print("Make sure the server is running.")
        return
    
    # Create 4 players with different colors
    p1 = Player(startPos[0], startPos[1], 60, 120, (0, 255, 0))     # Green - This player
    p2 = Player(50, 50, 60, 120, (255, 0, 0))                       # Red
    p3 = Player(50, 50, 60, 120, (0, 0, 255))                       # Blue
    p4 = Player(50, 50, 60, 120, (255, 255, 0))                     # Yellow
    other_players = [p2, p3, p4]
    
    # Deal hands - only for this player (p1)
    p1.set_tiles_hand(dg.get_tiles_hand())
    # Other players' hands are hidden/not shown
    
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        try:
            # Send this player's position, receive all other players' positions
            response = n.send(send_pos((p1.x, p1.y)))
            other_positions = read_all_players(response)
            
            # Update other players' positions
            for i, player in enumerate(other_players):
                if i < len(other_positions):
                    player.x = other_positions[i][0]
                    player.y = other_positions[i][1]
                    player.update()
                    
        except Exception as e:
            print(f"Connection lost: {e}")
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check both players' tile groups
                # for player in :
                    carrying_something = False
                    for sprite in p1.tiles_group:
                        if sprite.is_carried:
                            sprite.is_carried = False
                            carrying_something = True
                    if not carrying_something:
                        for sprite in reversed(p1.tiles_group.sprites()):
                            if sprite.check_click(event.pos):
                                break 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Rotate any carried tiles from both p1s
                    # for p1 in [p, p2]:
                        for sprite in p1.tiles_group:
                            if sprite.is_carried:
                                sprite.rotate()

        p1.move()

        # Update tiles
        p1.tiles_group.update()

        # Draw everything
        win.fill((255, 255, 255))
        for player in [p1, p2, p3, p4]:
            player.draw_tiles_hand(win)
        pygame.display.update()

main()