import numpy as np

from enum import Enum
from State import State
from Tile import Tile

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
        self.end_pos = None
        self.last_action = None
        self.steps = 0
        self.max_steps = None

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
                    self.end_pos = np.array([row, col])
                    tile_row.append(Tile.EMPTY)
                else: 
                    tile_row.append(tile_map[row][col])

            self.tile_map.append(tile_row)

    def set_max_steps(self, max_steps):
        self.max_steps = max_steps

    def is_empty(self, pos):
        row, col = pos
        if self.tile_map[row][col] != Tile.EMPTY:
            return False

        return True

    def is_out_of_bounds(self, pos):
        row, col = pos
        
        return row < 0 or row >= self.rows or col < 0 or col >= self.columns
    
    def is_on_air(self, pos):
        row, col = pos
        if row == 0:
            return False

        if self.tile_map[row-1][col] == Tile.BRICK:
            return False

        return True


    def step(self, action):
        # cannot jump while in mid air
        if action == Action.JUMP and self.is_on_air(self.current_pos):
            action = Action.NOTHING
            
        # update position
        new_pos = self.current_pos + action.get_delta()

        # check collision
        if self.is_out_of_bounds(new_pos) or not self.is_empty(new_pos):
            new_pos = self.current_pos

        # gravity
        if self.is_on_air(new_pos) and action != Action.JUMP:
            new_pos = new_pos - np.array([1, 0])

        self.current_pos = new_pos
        self.last_action = action
        self.steps += 1

    def __str__(self):
        tiles_str = 'agent: {}, state: {}\ngoal: {}\n'.format(self.current_pos, self.agent_state(), self.end_pos)

        for row in reversed(range(self.rows)):
            tiles_str += '|'
            for col in range(self.columns):
                if (self.current_pos == np.array([row, col])).all():
                    tiles_str += '*'
                elif (self.end_pos == np.array([row, col])).all():
                    tiles_str += 'o'
                elif self.tile_map[row][col] == Tile.BRICK:
                    tiles_str += Tile.BRICK.get_char()
                elif self.tile_map[row][col] == Tile.EMPTY:
                    tiles_str += Tile.EMPTY.get_char()
            tiles_str += '|\n'

        return tiles_str
    
    def agent_state(self):
        return State(self.current_pos, self.tile_map)

    def goal_achieved(self):
        return (self.current_pos == self.end_pos).all()

    def goal_surpassed(self):
        return self.current_pos[1] > self.end_pos[1]

    def max_steps_surpassed(self):
        if self.max_steps is None:
            return False
        return self.steps >= self.max_steps

    def finished_episode(self):
        return self.max_steps_surpassed() or self.goal_achieved() or self.goal_surpassed()
