#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import argparse
import math
import multiprocessing
# import pygame_plot
from numba import jit

#@jit(parallel=True, fastmath=True, nogil=True)
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
        if row_idx == grid.shape[0]-1: #last row
            pass
        else:
            #offset = (_iterations*2+1) - (row_idx*2+1) / 2
            offset = _iterations-row_idx-1
            significant_length = row_idx*2+1+1
            sub_row = row[offset:significant_length]
            processes =  []
            for i in range(1,len(sub_row)-2):
                p = multiprocessing.Process(target=proc_tri, args=(i, sub_row, binary_rule, case_val, grid, row_idx,))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
    return grid


# row_id * 2 + 1 = occupied cells, so remainder is (len(row) - occupied_cells)/2 which is the deadzone
def proc_tri(index, last_row, binary_rule, case_val, grid, row_idx):
    grid[row_idx+1][index+1] = binary_rule[case_val([int(last_row[index-1]), 
                                                 int(last_row[index]),
                                                 int(last_row[index+1])])]

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
