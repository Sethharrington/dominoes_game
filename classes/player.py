import pygame
from .tiles import Tile
from .domino_game import Domino_Game


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width  = width 
        self.height = width * 2
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3
        self.hand_picked = False
        self.hand = []
        self.tiles_group = pygame.sprite.Group()

    
    def set_tiles_hand(self, tiles_arr):
        """Set the tiles for this player (call once at game start)"""
        if len(self.hand) < 1:
            self.hand = tiles_arr
            count = 0
            for num_up, num_down in tiles_arr:
                new_tile = Tile(self.width, self.height, num_up, num_down, self.color, 
                               position_x=self.width*count+20, 
                               position_y=self.height*1+20)
                self.tiles_group.add(new_tile)
                count += 1
            self.hand_picked = True
    
    def draw_tiles_hand(self, surface):
        """Draw the player's tiles on the surface"""
        self.tiles_group.draw(surface)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()
    
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
