#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import argparse
import math
import cv2
import imutils

# import pygame_plot
from numba import jit

@jit(nopython=True, parallel=True, fastmath=True, nogil=True)
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
    pad = 1
    center = math.floor((_iterations*2+pad)/2)
    grid = np.zeros((_iterations, _iterations*2+pad))
    grid[0][center] = init
    for row_idx,row in enumerate(grid):
        if row_idx == 0:
            pass
        else:
            for col_idx,col in enumerate(row):
                #if col_idx < _iterations-(row_idx) or col_idx > 2*_iterations-(_iterations - (row_idx)):
                #    pass
                #else:
                grid[row_idx][col_idx] = binary_rule[case_val([int(grid[row_idx-1][col_idx-1]), 
                                                       int(grid[row_idx-1][col_idx]),
                                                       int(grid[row_idx-1][col_idx+1])])]
    return grid

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Automatons')
    parser.add_argument('rule', help='Choose a rule 0-255')
    parser.add_argument('iterations', help='Number of iterations to run')
    args = parser.parse_args()

    s = time.time()
    rule = int(args.rule)
    binary_rule = np.flip([rule >> i & 1 for i in range(7,-1,-1)])
    # binary_rule = np.logical_not(binary_rule).astype(int)
    iterations = int(args.iterations)
    init = 1
    pad = 1
    center = math.floor((iterations*2+pad)/2)
    grid = np.zeros((iterations, iterations*2+pad))
    #grid = np.random.choice(2,2*iterations**2, p=[0.005,0.995]).reshape(iterations,2*iterations).astype(float)
    grid[math.floor(iterations/2)][center] = init
    print("")
    print(grid)
    # kernel = np.concatenate((np.array([1,2,4]).reshape(3,1), np.zeros((3,2))), axis=1) # wow i made that super obfuscating
    kernel = np.array((
        [-1, 1, -1],
        [1, 1, 1],
        [-1, 1, -1]), dtype="int")

    for i in range(1000000):
        grid_correlated = cv2.filter2D(grid, -1, kernel).astype(int)
        grid = binary_rule[grid_correlated].astype(float)
        #grid_show = cv2.resize(grid, width=540, interpolation = cv2.INTER_NEAREST) 
        grid_show = imutils.resize(grid,width=1000)
        cv2.imshow("img",grid_show)
        time.sleep(.1)
        cv2.waitKey(10)
    cv2.filter2D(grid, -1, kernel).astype(int)
    #plt.show()
    e = time.time()

    print("Algorithm runs\t%s its\tin\t%s sec" % (iterations,e-s))
