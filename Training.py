import MapLoader
import numpy as np

from World import World, Action
from Tile import Tile
from Policy import GreedyPolicy
from Option import Option, PrimitiveOption
from QLearning import learn_episodic
from State import State

def training_base(name, options, map_file):
    print('Learning {}...'.format(name))
    training_map = MapLoader.open_file(map_file)

    # setup parameters
    max_episodes = 10000
    max_steps = 15
    alpha = lambda t: 0.5 * np.exp(-1*t/max_episodes)
    epsilon = lambda t: 0.3 * np.exp(-10*t/max_episodes)

    # reward function
    def reward_func(env):
        if env.goal_achieved():
            return 100
        elif env.max_steps_surpassed() or env.goal_surpassed():
            return -100
        else:
            return -10

    # world generator
    def world_gen(episode):
        w = World(training_map)
        w.set_max_steps(max_steps)

        return w

    if len(options) == 0:
        options = [ 
            PrimitiveOption(Action.NOTHING),
            PrimitiveOption(Action.WALK),
            PrimitiveOption(Action.JUMP),
        ]
    policy = GreedyPolicy(options)

    # learn the policy
    learn_episodic(
            world_gen=world_gen,
            policy=policy,
            reward_func=reward_func,
            max_episodes=max_episodes,
            alpha=alpha,
            epsilon=epsilon,
            discount_rate=0.95,
        )

    # print q table
    print(policy)
    policy.epsilon = 0

    return policy

def jump_slab():
    return training_base('jump slab', [], 'training_maps/jump_slab.map')


brick_ahead_floor = State((0,0), [[Tile.EMPTY, Tile.BRICK], [Tile.EMPTY, Tile.EMPTY]])
empty_ahead_floor = State((0,0), [[Tile.EMPTY, Tile.EMPTY], [Tile.EMPTY, Tile.EMPTY]])

def falling():
    # learn to climb slabs
    jump_slab_policy = jump_slab()
    # learn to fall and climb slabs
    jump_slab_option = Option(
            'CLIMB_SLAB',
            jump_slab_policy,
            lambda s: s == brick_ahead_floor,
            lambda s: s == empty_ahead_floor,
    )

    print('CLIMB_WALL will start when state is {}'.format(brick_ahead_floor))
    print('CLIMB_WALL will end when state is {}'.format(empty_ahead_floor))

    return training_base(
            'falling',
            [
                PrimitiveOption(Action.NOTHING),
                PrimitiveOption(Action.WALK),
                PrimitiveOption(Action.JUMP),
                jump_slab_option,
            ],
            'training_maps/falling.map'
    )
    
