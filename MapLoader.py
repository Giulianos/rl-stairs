from World import Tile

def open_file(path):
    map_file = open(path, 'r')

    file_rows = map_file.readlines()

    tiles = []
    for file_row in reversed(file_rows):
        tiles_row = []
        for file_char in file_row:
            if file_char == '0':
                tiles_row.append(Tile.EMPTY)
            elif file_char == '1':
                tiles_row.append(Tile.START)
            elif file_char == '2':
                tiles_row.append(Tile.END)
            elif file_char == '3':
                tiles_row.append(Tile.BRICK)

        tiles.append(tiles_row)

    map_file.close()

    return tiles
