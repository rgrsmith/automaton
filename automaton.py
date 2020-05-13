#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import argparse
import math
# import pygame_plot

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
    binary_rule = [_rule >> i & 1 for i in range(7,-1,-1)]
    case_val = lambda case : 7 - ((case[0])*4+(case[1])*2+(case[2]))
    pad = 3
    center = math.floor((_iterations*2+pad)/2)
    grid = np.zeros((_iterations, _iterations*2+pad),dtype='i1')
    grid[0][center] = init
    for row_idx,row in enumerate(grid):
        if row_idx == 0:
            pass
        else:
            for col_idx,col in enumerate(row):
                if col_idx < _iterations-(row_idx-1) or col_idx > 2*_iterations-(_iterations - (row_idx-1)):
                    pass
                else:
                    grid[row_idx][col_idx] = case_val([int(grid[row_idx-1][col_idx-1]), 
                                                       int(grid[row_idx-1][col_idx]),
                                                       int(grid[row_idx-1][col_idx+1])])
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
    plt.imshow(grid, cmap="gray_r")
    plt.savefig('aut.png')
    #plt.show()
    e = time.time()

    print("Algorithm runs\t%s its\tin\t%s sec" % (iterations,e-s))
