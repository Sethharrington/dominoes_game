import pygame
import sys

# Add project root to path

from network import *
from classes.tiles import Tile
from classes.domino_game import Domino_Game
from classes.player import *
from lib.utils import *

def main():
    pygame.init()


    # Starting a game
    new_game = Domino_Game()
    tiles = pygame.sprite.Group()
    
    while not exit:    
        
        # Clear screen first
        canvas.fill(bg)
        
        # Update tiles
        tiles.update()
        
        # Check collisions and update tile colors
        for sp in tiles:
            tiles.remove(sp)
            hits = pygame.sprite.spritecollide(sp, tiles, False)

            if hits:
                other_tile = hits[0]
                if sp.num_1 in [other_tile.num_1, other_tile.num_2] or sp.num_2 in [other_tile.num_1, other_tile.num_2]:
                    print("Match")
                    sp.draw_tile("green")
                else:
                    sp.draw_tile("red")
            else:
                sp.draw_tile()
            tiles.add(sp)
        
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                carrying_something = False
                for sprite in tiles:
                    if sprite.is_carried:
                        sprite.is_carried = False
                        carrying_something = True
                if not carrying_something:
                    for sprite in reversed(tiles.sprites()):
                        if sprite.check_click(event.pos):
                            break 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Rotate any carried tiles
                    for sprite in tiles:
                        if sprite.is_carried:
                            sprite.rotate()
            
main()