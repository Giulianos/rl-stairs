import MapLoader
import numpy as np

from World import World, Action
from Policy import GreedyPolicy
from Option import PrimitiveOption
from QLearning import learn_episodic

def training_base(name, options, map_file):
    print('Learning {}...'.format(name))
    training_map = MapLoader.open_file(map_file)

    # setup parameters
    max_episodes = 10000
    max_steps = 100
    total_max_steps = max_episodes*max_steps
    alpha = lambda t: 0.8 * np.exp(-1*t/total_max_steps)
    epsilon = lambda t: 0.5 * np.exp(-3*t/total_max_steps)

    # reward function
    def reward_func(env):
        if env.goal_achieved():
            return 1
        else:
            return -1

    if len(options) == 0:
        options = [ 
            PrimitiveOption(Action.NOTHING),
            PrimitiveOption(Action.WALK),
            PrimitiveOption(Action.JUMP),
        ]
    policy = GreedyPolicy(options)

    # learn the policy
    learn_episodic(
            world_gen=lambda e: World(training_map),
            policy=policy,
            reward_func=lambda env: 1 if env.goal_achieved() else -1,
            max_steps=max_steps,
            max_episodes=max_episodes,
            alpha=lambda t: 0.8 * np.exp(-1*t/max_steps),
            epsilon=lambda t: 0.5 * np.exp(-3*t/max_steps),
            discount_rate=0.9,
        )

    # print q table
    print(policy)
    policy.epsilon = 0

    return policy

def jump_slab():
    return training_base('jump slab', [], 'training_maps/jump_slab.map')
