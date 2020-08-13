from enum import Enum

class Tile(Enum):
    EMPTY = 0
    START = 1
    END = 2
    BRICK = 3

    def get_char(self):
        chars = [' ', 'X', 'X', 'O']

        return chars[self.value]

