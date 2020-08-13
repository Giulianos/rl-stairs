from Tile import Tile

class State:
    def __init__(self, agent_pos, tile_map):
        agent_row, agent_col = agent_pos
        map_rows, map_cols = len(tile_map), len(tile_map[0])
        if agent_col == map_cols-1:
            self.front = True
            self.top_front = True
        elif agent_row == map_rows-1:
            self.top_front = True
            self.front = tile_map[agent_row][agent_col+1] == Tile.BRICK
        else:
            self.top_front = tile_map[agent_row+1][agent_col+1] == Tile.BRICK
            self.front = tile_map[agent_row][agent_col+1] == Tile.BRICK

        self.floor = agent_row == 0 or tile_map[agent_row-1][agent_col] == Tile.BRICK

    def __eq__(self, other):
        return self.front == other.front and self.top_front == other.top_front and self.floor == other.floor

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.front, self.top_front, self.floor))
    
    def __str__(self):
        s = '_' if self.floor else ' '
        if self.front and self.top_front:
            s += ':'
        elif self.front and not self.top_front:
            s += '.'
        elif not self.front and self.top_front:
            s += '˙'
        else:
            s += ' '

        return s

    def __repr__(self):
        return str(self)

