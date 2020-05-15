#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import argparse
import math
import cv2
import imutils

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Automatons')
    parser.add_argument('rule', help='Choose a rule 0-255')
    parser.add_argument('iterations', help='Number of iterations to run')
    args = parser.parse_args()

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

    kernel = np.array((
        [-1, 1, -1],
        [1, 1, 1],
        [-1, 1, -1]), dtype="int")
    
    s = time.time()

    while True:
        grid_correlated = cv2.filter2D(grid, -1, kernel).astype(int)
        grid = binary_rule[grid_correlated].astype(float)
        #grid_show = cv2.resize(grid, width=540, interpolation = cv2.INTER_NEAREST) 
        grid_show = imutils.resize(grid,width=1000)
        cv2.imshow("img",grid_show)
        cv2.waitKey(100)
        e = time.time()
        print('Framerate: %i FPS\r'%(1.0/(e-s)), end="")
        s = time.time()
