import MapLoader
import Training
import numpy as np

from World import World
from World import Action

policy = Training.falling()

# load test map from file
test_map = MapLoader.open_file('test_maps/falling.map')

# create world from loaded map
test_world = World(test_map)
print(test_world)

# test policy
while True:
    key = input('')
    if key == 'q':
        break

    # get action from learned policy
    a = policy.action(test_world.agent_state())
    print(policy.current_option.name)

    # perform action
    test_world.step(a)

    print(test_world)

    if test_world.goal_achieved():
        print('Goal achieved, restarting world...')
        test_world = World(test_map)
        print(test_world)

