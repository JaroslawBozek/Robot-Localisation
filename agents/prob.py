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
        self.first_move_made = False


        # self.P = None
        prob = 1.0 / len(self.locations)
        self.P = prob * np.ones([len(self.locations)], dtype=np.float)
        self.P = np.array([self.P, self.P, self.P, self.P])


    def __call__(self, percept):

        #NESW #Each dimension assumes that the robot starts in a position of N,E,S,W
        # update posterior
        print(self.prev_action)
        out_T = np.eye(len(self.locations))
        out_T = np.array([out_T,out_T,out_T,out_T])
        if self.prev_action == 'forward':
            for i1, loc1 in enumerate(self.locations):
                for i2, loc2 in enumerate(self.locations):
                    loc_N = (loc1[0], loc1[1] + 1)
                    loc_E = (loc1[0] + 1, loc1[1])
                    loc_S = (loc1[0], loc1[1] - 1)
                    loc_W = (loc1[0] - 1, loc1[1])



                    locs = [loc_N,loc_E,loc_S,loc_W]
                    for j, loc in enumerate(locs):
                        if loc1 == loc2:
                            if loc in self.walls:
                                out_T[j][i1][i2] = 1.
                            else:
                                out_T[j][i1][i2] = 0.05
                        else:
                            if loc == loc2:
                                out_T[j][i1][i2] = 0.95
                            else:
                                out_T[j][i1][i2] = 0.

        if self.prev_action == 'turnleft':
            new_self_P = np.ones([len(self.locations)], dtype=np.float)
            new_self_P = np.array([new_self_P, new_self_P, new_self_P, new_self_P])

            new_self_P[0] = (0.05 * self.P[0]) + (0.95 * self.P[1])
            new_self_P[1] = (0.05 * self.P[1]) + (0.95 * self.P[2])
            new_self_P[2] = (0.05 * self.P[2]) + (0.95 * self.P[3])
            new_self_P[3] = (0.05 * self.P[3]) + (0.95 * self.P[0])
            self.P = new_self_P

        if self.prev_action == 'turnright':
            new_self_P = np.ones([len(self.locations)], dtype=np.float)
            new_self_P = np.array([new_self_P, new_self_P, new_self_P, new_self_P])

            new_self_P[0] = (0.05 * self.P[0]) + (0.95 * self.P[3])
            new_self_P[1] = (0.05 * self.P[1]) + (0.95 * self.P[0])
            new_self_P[2] = (0.05 * self.P[2]) + (0.95 * self.P[1])
            new_self_P[3] = (0.05 * self.P[3]) + (0.95 * self.P[2])
            self.P = new_self_P

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
            loc_W = False

            if (loc[0], loc[1] + 1) in self.walls:
                loc_N = True
            if (loc[0] + 1, loc[1]) in self.walls:
                loc_E = True
            if (loc[0], loc[1] - 1) in self.walls:
                loc_S = True
            if (loc[0] - 1, loc[1]) in self.walls:
                loc_W = True

            #Poprawione dla różnych rozmiarów map
            if loc[0] == 0:
                loc_W = True
            if loc[0] == self.size-1:
                loc_E = True
            if loc[1] == 0:
                loc_S = True
            if loc[1] == self.size-1:
                loc_N = True

            percept_info = ['fwd', 'left', 'bckwd', 'right']
            locs = [loc_N, loc_E, loc_S, loc_W]

            #Check forward
            if 'fwd' in percept:
                if loc_N == True:
                    prob_N = prob_N * 0.9
                else:
                    prob_N = prob_N * 0.1
                if loc_E == True:
                    prob_E = prob_E * 0.9
                else:
                    prob_E = prob_E * 0.1
                if loc_S == True:
                    prob_S = prob_S * 0.9
                else:
                    prob_S = prob_S * 0.1
                if loc_W == True:
                    prob_W = prob_W * 0.9
                else:
                    prob_W = prob_W * 0.1
            else:
                if loc_N == True:
                    prob_N = prob_N * 0.1
                else:
                    prob_N = prob_N * 0.9
                if loc_E == True:
                    prob_E = prob_E * 0.1
                else:
                    prob_E = prob_E * 0.9
                if loc_S == True:
                    prob_S = prob_S * 0.1
                else:
                    prob_S = prob_S * 0.9
                if loc_W == True:
                    prob_W = prob_W * 0.1
                else:
                    prob_W = prob_W * 0.9
            #Check left
            if 'left' in percept:
                if loc_N == True:
                    prob_E = prob_E * 0.9
                else:
                    prob_E = prob_E * 0.1
                if loc_E == True:
                    prob_S = prob_S * 0.9
                else:
                    prob_S = prob_S * 0.1
                if loc_S == True:
                    prob_W = prob_W * 0.9
                else:
                    prob_W = prob_W * 0.1
                if loc_W == True:
                    prob_N = prob_N * 0.9
                else:
                    prob_N = prob_N * 0.1
            else:
                if loc_N == True:
                    prob_E = prob_E * 0.1
                else:
                    prob_E = prob_E * 0.9
                if loc_E == True:
                    prob_S = prob_S * 0.1
                else:
                    prob_S = prob_S * 0.9
                if loc_S == True:
                    prob_W = prob_W * 0.1
                else:
                    prob_W = prob_W * 0.9
                if loc_W == True:
                    prob_N = prob_N * 0.1
                else:
                    prob_N = prob_N * 0.9

            # Check backward
            if 'bckwd' in percept:
                if loc_N == True:
                    prob_S = prob_S * 0.9
                else:
                    prob_S = prob_S * 0.1
                if loc_E == True:
                    prob_W = prob_W * 0.9
                else:
                    prob_W = prob_W * 0.1
                if loc_S == True:
                    prob_N = prob_N * 0.9
                else:
                    prob_N = prob_N * 0.1
                if loc_W == True:
                    prob_E = prob_E * 0.9
                else:
                    prob_E = prob_E * 0.1
            else:
                if loc_N == True:
                    prob_S = prob_S * 0.1
                else:
                    prob_S = prob_S * 0.9
                if loc_E == True:
                    prob_W = prob_W * 0.1
                else:
                    prob_W = prob_W * 0.9
                if loc_S == True:
                    prob_N = prob_N * 0.1
                else:
                    prob_N = prob_N * 0.9
                if loc_W == True:
                    prob_E = prob_E * 0.1
                else:
                    prob_E = prob_E * 0.9

            if 'right' in percept:
                if loc_N == True:
                    prob_W = prob_W * 0.9
                else:
                    prob_W = prob_W * 0.1
                if loc_E == True:
                    prob_N = prob_N * 0.9
                else:
                    prob_N = prob_N * 0.1
                if loc_S == True:
                    prob_E = prob_E * 0.9
                else:
                    prob_E = prob_E * 0.1
                if loc_W == True:
                    prob_S = prob_S * 0.9
                else:
                    prob_S = prob_S * 0.1
            else:
                if loc_N == True:
                    prob_W = prob_W * 0.1
                else:
                    prob_W = prob_W * 0.9
                if loc_E == True:
                    prob_N = prob_N * 0.1
                else:
                    prob_N = prob_N * 0.9
                if loc_S == True:
                    prob_E = prob_E * 0.1
                else:
                    prob_E = prob_E * 0.9
                if loc_W == True:
                    prob_S = prob_S * 0.1
                else:
                    prob_S = prob_S * 0.9

            #Dodano Bump
            #Jeśli otrzymano informację 'bump' to zostają tylko lokacje, które są zwrócone w kierunku ściany.
            if 'bump' in percept:
                if loc_N == False:
                    prob_N = 0
                if loc_E == False:
                    prob_E = 0
                if loc_S == False:
                    prob_S = 0
                if loc_W == False:
                    prob_W = 0

            out_N = np.append(out_N, prob_N)
            out_E = np.append(out_E, prob_E)
            out_S = np.append(out_S, prob_S)
            out_W = np.append(out_W, prob_W)

        self.out_O = np.array([out_N, out_E, out_S, out_W])
        self.out_T = out_T

        print(self.out_O.shape)
        #Planning

        if 'fwd' in percept:
            if 'right' not in percept:
                action = 'turnright'
            else:
                action = 'turnleft'
        else:
            action = 'forward'


        self.prev_action = action

        return action

    def getPosterior(self):
        # directions in order 'N', 'E', 'S', 'W'

        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)


        out_P_N = self.out_O[0] * np.dot(self.out_T[0].T, self.P[0])
        out_P_E = self.out_O[1] * np.dot(self.out_T[1].T, self.P[1])
        out_P_S = self.out_O[2] * np.dot(self.out_T[2].T, self.P[2])
        out_P_W = self.out_O[3] * np.dot(self.out_T[3].T, self.P[3])
        out_P = np.array([out_P_N, out_P_E, out_P_S, out_P_W])

        for i, loc in enumerate(self.locations):
            for j in range(4):
                P_arr[loc[0]][loc[1]][j] = out_P[j][i]

        self.P = out_P / np.sum(out_P)
        P_arr = (P_arr/np.sum(P_arr))
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
