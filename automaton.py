#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import argparse
import math

def automaton(rule,case):
    """ rule : [int] choice of rule for automaton (betwee 0 and 255)
        case : [int,int,int] three cell occupancy 
    """
    if rule >=0 and rule <=255:
        _rule = int(rule)
    else:
        print("Rule must be an int between 0 and 255")
        return
    binary_rule = [_rule >> i & 1 for i in range(7,-1,-1)]
    if len(case) == 3:
        _case_val = 7 - int((case[0])*4+(case[1])*2+(case[2]))
        # print("Case Val = %s from: %s using rule: %s" % (_case_val, case, binary_rule))
    #print("Binary Rule: %s" % binary_rule)
    cell_occupancy = []
    return int(binary_rule[_case_val])

def CellularAutomaton(rule,init,t):
    """ rule : [int] choice of rule between 0 and 255
        init : [int] choice of initial condition either 0 or 1
        t    : [int] number of iterations
    """
    if rule >=0 and rule <=255:
        _rule = int(rule)
    else:
        print("Rule must be an int between 0 and 255")
        return
    _iterations = t
    if not _iterations % 2:      # even
        pad = 3
        center = math.floor((_iterations*2+pad)/2)
    else:                       # odd
        pad = 4
        center = math.floor((_iterations*2+pad)/2)
    # grid = np.array([np.array([0 for i in range(iterations+pad)]) for i in range(iterations)])
    grid = np.zeros((_iterations, _iterations*2+pad))
    grid[0][center] = init
    #for iteration in range(_iterations):
    for row_idx,row in enumerate(grid):
        if row_idx == 0:
            pass
        else:
            for col_idx,col in enumerate(row):
                if col_idx == 0 or col_idx == len(row)-1:
                    pass
                else:
                    upper_triad = [int(grid[row_idx-1][col_idx-1]), 
                                   int(grid[row_idx-1][col_idx]),
                                   int(grid[row_idx-1][col_idx+1])]
                    grid[row_idx][col_idx] = automaton(_rule,upper_triad)
                #print("Row: %i\t Col: %i" % (row_idx, col_idx))
                #print("sending to automaton: %s" % upper_triad)
                #print("Assigning Grid Val: %i" % grid[row_idx][col_idx])
        # print(grid)
    return grid

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Automatons')
    parser.add_argument('rule', help='Choose a rule 0-255')
    parser.add_argument('iterations', help='Number of iterations to run')
    args = parser.parse_args()
    s = time.time()
    rule = int(args.rule)
    iterations = int(args.iterations)
    grid = CellularAutomaton(rule,1,iterations)
    e = time.time()
    print("Algorithm runs\t%s its\tin\t%s sec" % (iterations,e-s))
    plt.imshow(grid, cmap="gray_r")
    plt.show()
