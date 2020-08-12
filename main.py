from World import World
from World import Action

import MapLoader

tile_map = MapLoader.open_file('sample_map.txt')
world = World(tile_map)

print(world.print())
key = input('')
while key is not 'q':
    action = None
    if key == 'w' or key == 'W':
        action = Action.WALK
    elif key == 'n' or key == 'N':
        action = Action.NOTHING
    elif key == 'j' or key == 'J':
        action = Action.JUMP

    if action is None:
        print('Comando invalido')
    else:
        world.step(action)
        print(world.print())
        
    key = input('')
