import numpy as np
from enum import Enum

class Tile(Enum):
    EMPTY = 0
    START = 1
    END = 2
    BRICK = 3

    def get_char(self):
        chars = [' ', 'X', 'X', 'O']

        return chars[self.value]

class Action(Enum):
    NOTHING = 0
    WALK = 1
    JUMP = 2

    def get_delta(self):
        deltas = [ [0,0], [0,1], [1,0] ]
        
        return deltas[self.value]

class World:
    def __init__(self, tile_map):
        self.current_pos = None
        self.end = None
        self.last_action = None

        self.rows = len(tile_map)
        self.columns = len(tile_map[0])

        # build map removing start and end markers
        self.tile_map = []
        for row in range(self.rows):
            tile_row = []
            for col in range(self.columns):
                if tile_map[row][col] == Tile.START:
                    self.current_pos = np.array([row, col])
                    tile_row.append(Tile.EMPTY)
                elif tile_map[row][col] == Tile.END:
                    self.end = np.array([row, col])
                    tile_row.append(Tile.EMPTY)
                else: 
                    tile_row.append(tile_map[row][col])

            self.tile_map.append(tile_row)

    def is_empty(self, pos):
        row, col = pos
        if self.tile_map[row][col] != Tile.EMPTY:
            return False

        return True
    
    def is_on_air(self, pos):
        row, col = pos
        if row == 0:
            return False

        if self.tile_map[row-1][col] == Tile.BRICK:
            return False

        return True


    def step(self, action):
        # cannot walk more than one step on the air
        if action == Action.WALK and self.last_action == Action.WALK:
            print('cannot walk more than one step on the air')
            action = Action.NOTHING

        # cannot jump while in mid air
        if action == Action.JUMP and self.is_on_air(self.current_pos):
            print('cannot jump while in mid air')
            action = Action.NOTHING
            
        # update position
        new_pos = self.current_pos + action.get_delta()

        # check collision
        if not self.is_empty(new_pos):
            print('collision')
            new_pos = current_pos

        # gravity
        if self.is_on_air(new_pos) and action != Action.JUMP:
            print('fall')
            new_pos = new_pos - np.array([1, 0])

        self.current_pos = new_pos
        self.last_action = action

    def print(self):
        tiles_str = ""

        for row in reversed(range(self.rows)):
            for col in range(self.columns):
                if (self.current_pos == np.array([row, col])).all():
                    tiles_str += '*'
                elif self.tile_map[row][col] == Tile.BRICK:
                    tiles_str += Tile.BRICK.get_char()
                elif self.tile_map[row][col] == Tile.EMPTY:
                    tiles_str += Tile.EMPTY.get_char()
            tiles_str += '\n'

        return tiles_str
