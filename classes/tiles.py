import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, width, height, number_up_right, number_down_left, rect_color = (50,50,50), points_color = (0, 0, 0), position_x=0, position_y=0, orientation = "UP"):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.set_position(position_x, position_y)
        self.rect.topleft = (self.position_x, self.position_y)
        self.width = width
        self.height = height
        self.num_1 = number_up_right
        self.num_2 = number_down_left
        self.color = rect_color
        self.points_color = points_color
        self.orientation = orientation
        self.grid_size = (self.width)/(3*2)
        self.draw_tile()
        self.is_carried = False
    
    def get_point_position(self, number):
        # The half of the dominoe tile is divided in a grid of 9 squares, the grid_size if the size of the half of those squares
        positions_array = []
        if(number != 0): 
            if(number == 1): 
                positions_array = [[2,2]]
            elif(number == 2 and self.orientation in ["UP", "DOWN"] ): 
                positions_array = [[1,3],[3,1]]
            elif(number == 3 and self.orientation in ["UP", "DOWN"]): 
                positions_array = [[1,3],[2,2],[3,1]]
            elif(number == 4): 
                positions_array = [[1,1],[1,3],[3,1],[3,3]]
            elif(number == 5): 
                positions_array = [[1,1],[1,3],[2,2],[3,1],[3,3]]
            elif(number == 6 and self.orientation in ["UP", "DOWN"]): 
                positions_array = [[1,1],[1,3],[1,2],[3,1],[3,2],[3,3]]
            elif(number == 2): 
                positions_array = [[1,1],[3,3]]
            elif(number == 3): 
                positions_array = [[1,1],[2,2],[3,3]]
            elif(number == 6): 
                positions_array = [[1,1],[2,1],[3,1],[1,3],[2,3],[3,3]]
        return positions_array

    def draw_points(self, positions_array, is_first_half):
        second_half_offset_x = 0
        second_half_offset_y = 0
        if(is_first_half):
            if(self.orientation in ["UP", "DOWN"]):
                second_half_offset_y = self.height/2
            else:
                second_half_offset_x = self.width/2
        for x,y in positions_array:
            position_point_x = self.grid_size * (x+1) + second_half_offset_x
            position_point_y = self.grid_size * (y+1) + second_half_offset_y
            pygame.draw.circle(self.image, self.points_color, (position_point_x,position_point_y),3,0)
    
    def set_position(self,position_x=0, position_y=0 ):
        self.position_x = position_x
        self. position_y = position_y

    def set_orientation(self, is_vertical):
        self.orientation = is_vertical

    def update(self):
        if self.is_carried:
            self.rect.center = pygame.mouse.get_pos()

    def draw_tile(self, bg_color = "white"):   
        self.image.fill(bg_color)
        if self.orientation in ["UP", "DOWN"]:
            pygame.draw.rect(self.image, self.color, 
                         pygame.Rect(0, 0, self.width, self.height), 4)
            pygame.draw.line(self.image, self.color, (0, self.height/2), (self.width, self.height/2), 4)
        else:
            pygame.draw.rect(self.image, self.color, 
                         pygame.Rect(0, 0, self.width, self.height), 4)
            pygame.draw.line(self.image, self.color, (self.width/2, 0), (self.width/2, self.height), 4)
        
        self.draw_points(self.get_point_position(self.num_1), True)
        self.draw_points(self.get_point_position(self.num_2), False)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse clicked inside this sprite's rect
            if self.rect.collidepoint(event.pos):
                self.dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Move the rect by the relative movement of the mouse
                self.rect.move_ip(event.rel)
    
    def check_click(self, mouse_pos):
        """Checks if this sprite was clicked and returns True if it was."""
        if self.rect.collidepoint(mouse_pos):
            self.is_carried = not self.is_carried
            return True
        return False
    
    def rotate(self):
        old_center = self.rect.center  # Preserve position

        if self.orientation == "UP":
            self.orientation = "RIGHT"

        elif self.orientation == "RIGHT":
            self.orientation = "DOWN"
            self.num_1, self.num_2 = self.num_2, self.num_1
            
        elif self.orientation == "DOWN":
            self.orientation = "LEFT"
            
        elif self.orientation == "LEFT":
            self.orientation = "UP"
            self.num_1, self.num_2 = self.num_2, self.num_1
            
        self.height, self.width = self.width, self.height
        # Recreate surface with new dimensions
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Redraw the tile
        self.draw_tile()
        
        # Update rect and preserve center position
        self.rect = self.image.get_rect()
        self.rect.center = old_center