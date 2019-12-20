map = [
    [26, 26, 26, 26, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33],
    [26, 26, 15, 15, 26, 26, 26, 26, 33, 33, 33, 33, 33, 33, 33],
    [26, 26, 16, 15, 26, 26, 26, 26, 26, 26, 26, 33, 33, 33, 33],
    [25, 25, 25, 25, 25, 25, 25, 25, 15, 26, 26, 26, 33, 33, 33],
    [15, 25, 25, 25, 25, 25, 25, 25, 25, 15, 26, 33, 33, 33, 33],
    [26, 15, 15, 15, 25, 25, 25, 25, 15, 26, 33, 33, 33, 33, 33],
    [33, 26, 15, 26, 15, 25, 25, 15, 15, 26, 33, 33, 33, 33, 33],
    [33, 33, 33, 33, 26, 15, 25, 25, 15, 26, 33, 33, 33, 33, 33],
    [33, 33, 33, 33, 33, 26, 15, 25, 25, 15, 33, 33, 33, 33, 33],
    [33, 33, 33, 33, 33, 33, 26, 15, 15, 15, 33, 33, 33, 33, 33],
    [33, 33, 33, 33, 33, 33, 26, 26, 26, 26, 33, 33, 33, 33, 33],
    [33, 33, 33, 33, 33, 33, 26, 26, 26, 26, 26, 33, 33, 33, 33],
    [33, 33, 33, 33, 33, 26, 26, 26, 26, 26, 26, 33, 33, 33, 33]
]

import numpy as np
import sys
from gym.envs.toy_text import discrete

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class ShrineOfFiendsEnv(discrete.DiscreteEnv):

    metadata = {'render.modes': ['human', 'ansi']}

    def __init__(self, shape=[13, 15], composite_grid=map):
        self.shape = np.array(shape)
        # Nature of overworld navigation in FF mercifully means that the PC is in a static position and game moves around him
        self.start_state_index = np.ravel_multi_index((9, 8), self.shape)
        self.composite_grid = composite_grid

        nS = np.prod(self.shape)
        nA = 4

        MAX_Y = shape[0]
        MAX_X = shape[1]

        # Initialize transition probabilities and rewards
        P = {}
        grid = np.arange(nS).reshape(shape)
        it = np.nditer(grid, flags=['multi_index'])

        while not it.finished:
            s = it.iterindex
            y, x = it.multi_index

            P[s] = {a : [] for a in range(nA)}

            is_done = lambda y, x: self.composite_grid[y][x] == 16
            reward = 1.0 if is_done(y, x) else -1.0

            # We're stuck in a terminal state
            if is_done(y, x):
                P[s][UP] = [(1.0, s, reward, True)]
                P[s][RIGHT] = [(1.0, s, reward, True)]
                P[s][DOWN] = [(1.0, s, reward, True)]
                P[s][LEFT] = [(1.0, s, reward, True)]
            # Not a terminal state
            else:
                ns_up = s if y == 0 else s - MAX_X
                ns_right = s if x == (MAX_X - 1) else s + 1
                ns_down = s if y == (MAX_Y - 1) else s + MAX_X
                ns_left = s if x == 0 else s - 1
                P[s][UP] = [(1.0, ns_up, reward, is_done(y, x))]
                P[s][RIGHT] = [(1.0, ns_right, reward, is_done(y, x))]
                P[s][DOWN] = [(1.0, ns_down, reward, is_done(y, x))]
                P[s][LEFT] = [(1.0, ns_left, reward, is_done(y, x))]

            it.iternext()

        # Initial state distribution is uniform
        isd = np.ones(nS) / nS

        # We expose the model of the environment for educational purposes
        # This should not be used in any model-free learning algorithm
        self.P = P

        super(ShrineOfFiendsEnv, self).__init__(nS, nA, P, isd)


    def render(self, mode='human'):
        outfile = sys.stdout

        for s in range(self.nS):
            position = np.unravel_index(s, self.shape)
            # Player character location
            if self.s == s:
                output = " @ "
            # Reward point. For Shrine of Fiends test, we're going to hardcode this as the only 16 that showed up. This might not even be accurate, but it does enable testing in a vacuum
            # This, along with the character state identifications, is one of the core sensory heuristics I need to work on
            elif self.composite_grid[position[0]][position[1]] == 16:
                output = " * "
            # Water tiles. Impassible w/o boat
            elif self.composite_grid[position[0]][position[1]] == 33:
                output = " B "
            # Forest or meadows. Might have random encounters
            elif self.composite_grid[position[0]][position[1]] == 25 or self.composite_grid[position[0]][position[1]] == 26:
                output = " G "
            # Probably black, given the color's role in literally outlining the universe
            elif self.composite_grid[position[0]][position[1]] == 15:
                output = " ? "

            if position[1] == 0:
                output = output.lstrip()
            if position[1] == self.shape[1] - 1:
                output = output.rstrip()
                output += '\n'

            outfile.write(output)
        outfile.write('\n')


ShrineOfFiendsEnv().render()
