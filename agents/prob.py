# prob.py
# This is

import random
import numpy as np
import sys
from gridutil import *

best_turn = {('N', 'E'): 'turnright',
             ('N', 'S'): 'turnright',
             ('N', 'W'): 'turnleft',
             ('E', 'S'): 'turnright',
             ('E', 'W'): 'turnright',
             ('E', 'N'): 'turnleft',
             ('S', 'W'): 'turnright',
             ('S', 'N'): 'turnright',
             ('S', 'E'): 'turnleft',
             ('W', 'N'): 'turnright',
             ('W', 'E'): 'turnright',
             ('W', 'S'): 'turnleft'}


class LocAgent:

    def __init__(self, size, walls, eps_perc, eps_move):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.eps_perc = eps_perc
        self.eps_move = eps_move
        # whether to plan next direction to move
        self.plan_next_move = True
        # planned direction
        self.next_dir = None
        # previous action
        self.prev_action = None


        # self.P = None
        prob = 1.0 / len(self.locations)
        self.P = prob * np.ones([len(self.locations)], dtype=np.float)

    def __call__(self, percept):

        #NESW #Each dimension assumes that the robot starts in a position of N,E,S,W
        # update posterior
        print(self.prev_action)
        out_T = np.eye(len(self.locations))
        out_T = np.array([out_T,out_T,out_T,out_T])

        print(self.locations)
        print(out_T.shape)


        if self.prev_action == 'forward':
            for i1, loc1 in enumerate(self.locations):
                for i2, loc2 in enumerate(self.locations):
                    loc_N = (loc1[0], loc1[1] + 1)
                    loc_E = (loc1[0] + 1, loc1[1])
                    loc_S = (loc1[0], loc1[1] - 1)
                    loc_W = (loc1[0] - 1, loc1[1])


                    if loc1 == loc2:
                        if loc_N in self.walls:
                            out_T[0][i1][i2] = 1.
                        else:
                            out_T[0][i1][i2] = 0.05
                    else:
                        if loc_N == loc2:
                            out_T[0][i1][i2] = 0.95
                        else:
                            out_T[0][i1][i2] = 0.

                    if loc1 == loc2:
                        if loc_E in self.walls:
                            out_T[1][i1][i2] = 1.
                        else:
                            out_T[1][i1][i2] = 0.05
                    else:
                        if loc_E == loc2:
                            out_T[1][i1][i2] = 0.95
                        else:
                            out_T[1][i1][i2] = 0.

                    if loc1 == loc2:
                        if loc_S in self.walls:
                            out_T[2][i1][i2] = 1.
                        else:
                            out_T[2][i1][i2] = 0.05
                    else:
                        if loc_S == loc2:
                            out_T[2][i1][i2] = 0.95
                        else:
                            out_T[2][i1][i2] = 0.

                    if loc1 == loc2:
                        if loc_W in self.walls:
                            out_T[3][i1][i2] = 1.
                        else:
                            out_T[3][i1][i2] = 0.05
                    else:
                        if loc_W == loc2:
                            out_T[3][i1][i2] = 0.95
                        else:
                            out_T[3][i1][i2] = 0.

        print(out_T)

        out_N = np.array([])
        out_E = np.array([])
        out_S = np.array([])
        out_W = np.array([])
        for i, loc in enumerate(self.locations):
            prob_N = 1.0
            prob_E = 1.0
            prob_S = 1.0
            prob_W = 1.0

            loc_N = False
            loc_E = False
            loc_S = False
            Loc_W = False

            if (loc[0], loc[1]+1) in self.walls:
                loc_N = True
            if (loc[0] + 1, loc[1]) in self.walls:
                loc_E = True
            if (loc[0], loc[1] - 1) in self.walls:
                loc_S = True
            if (loc[0] - 1, loc[1]) in self.walls:
                loc_W = True

            # if 'fwd' in percept:
            #     if (loc[0], loc[1]+1) in self.walls:
            #         prob_N = prob_N*0.9
            #     else:
            #         prob_N = prob_N*0.1
            #     if (loc[0] + 1, loc[1]) in self.walls:
            #         prob_E = prob_E * 0.9
            #     else:
            #         prob_E = prob_E * 0.1
            #     if (loc[0], loc[1] - 1) in self.walls:
            #         prob_S = prob_S * 0.9
            #     else:
            #         prob_S = prob_S * 0.1
            #     if (loc[0] - 1, loc[1]) in self.walls:
            #         prob_W = prob_W * 0.9
            #     else:
            #         prob_W = prob_W * 0.1
            #
            # if 'left' in percept:
            #     if (loc[0], loc[1]+1) in self.walls:
            #         prob_E = prob_E*0.9
            #     else:
            #         prob_E = prob_E*0.1
            #     if (loc[0] + 1, loc[1]) in self.walls:
            #         prob_S = prob_S * 0.9
            #     else:
            #         prob_S = prob_S * 0.1
            #     if (loc[0], loc[1] - 1) in self.walls:
            #         prob_W = prob_W * 0.9
            #     else:
            #         prob_W = prob_W * 0.1
            #     if (loc[0] - 1, loc[1]) in self.walls:
            #         prob_N = prob_N * 0.9
            #     else:
            #         prob_N = prob_N * 0.1
            #
            # if 'bckwd' in percept:
            #     if (loc[0], loc[1]+1) in self.walls:
            #         prob_S = prob_S*0.9
            #     else:
            #         prob_S = prob_S*0.1
            #     if (loc[0] + 1, loc[1]) in self.walls:
            #         prob_W = prob_W * 0.9
            #     else:
            #         prob_W = prob_W * 0.1
            #     if (loc[0], loc[1] - 1) in self.walls:
            #         prob_N = prob_N * 0.9
            #     else:
            #         prob_N = prob_N * 0.1
            #     if (loc[0] - 1, loc[1]) in self.walls:
            #         prob_E = prob_E * 0.9
            #     else:
            #         prob_E = prob_E * 0.1
            #
            # if 'right' in percept:
            #     if (loc[0], loc[1]+1) in self.walls:
            #         prob_W = prob_W*0.9
            #     else:
            #         prob_W = prob_W*0.1
            #     if (loc[0] + 1, loc[1]) in self.walls:
            #         prob_N = prob_N * 0.9
            #     else:
            #         prob_N = prob_N * 0.1
            #     if (loc[0], loc[1] - 1) in self.walls:
            #         prob_E = prob_E * 0.9
            #     else:
            #         prob_E = prob_E * 0.1
            #     if (loc[0] - 1, loc[1]) in self.walls:
            #         prob_S = prob_S * 0.9
            #     else:
            #         prob_S = prob_S * 0.1

            out_N = np.append(out_N, prob_N)
            out_E = np.append(out_E, prob_E)
            out_S = np.append(out_S, prob_S)
            out_W = np.append(out_W, prob_W)

        print(out_N,out_E,out_S,out_W)
        #TODO PUT YOUR CODE HERE


        # -----------------------

        action = 'forward'
        # TODO CHANGE THIS HEURISTICS TO SPEED UP CONVERGENCE
        # if there is a wall ahead then lets turn
        if 'fwd' in percept:
            # higher chance of turning left to avoid getting stuck in one location
            action = np.random.choice(['turnleft', 'turnright'], 1, p=[0.8, 0.2])
        else:
            # prefer moving forward to explore
            action = np.random.choice(['forward', 'turnleft', 'turnright'], 1, p=[0.8, 0.1, 0.1])

        self.prev_action = action

        return action

    def getPosterior(self):
        # directions in order 'N', 'E', 'S', 'W'
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)

        # put probabilities in the array
        # TODO PUT YOUR CODE HERE


        # -----------------------

        return P_arr

    def forward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    def backward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    @staticmethod
    def turnright(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 1) % 4
        return cur_loc, dirs[idx]

    @staticmethod
    def turnleft(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 4 - 1) % 4
        return cur_loc, dirs[idx]
