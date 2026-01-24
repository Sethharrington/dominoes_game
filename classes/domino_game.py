import random
class Domino_Game:
    def __init__(self):
        self.tiles = [[i,j] for i in range(0,7) for j in range(i,7)]
        self.tiles_hands_left = self.tiles.copy()  # Make a copy!
        self.left_tile = 0
        self.right_tile = 0

    def get_tiles_nums_arr(self):
        return self.tiles

    def get_tiles_hand(self):
        hand_arr = []
        for i in range(0,7):
            rand_tile_index = random.randint(0,len(self.tiles_hands_left)-1)
            print(rand_tile_index)
            hand_arr.append(self.tiles_hands_left[rand_tile_index])
            self.tiles_hands_left.remove(self.tiles_hands_left[rand_tile_index])
            print(hand_arr)
        return hand_arr
    def get_tiles_group(self, tiles_arr, Tile, tiles_group):
        for i in range(0,4):
            count = 0
            