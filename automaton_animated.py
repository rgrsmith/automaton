#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import argparse
import math
import cv2
import imutils

class Range(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def __eq__(self, other):
        return self.start <= other <= self.end

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Automatons')
    parser.add_argument('-r', '--rule', type=int, default=42, help='Choose a rule 0-255')
    parser.add_argument('-i', '--iterations', type=int, default=500, help='Number of iterations to run')
    parser.add_argument('-f', '--framerate', type=float, default=10, help='attempt to run at given framerate FPS')
    parser.add_argument('-d', '--demo', help='Run demo mode with preset pretty thing', action='store_true')
    parser.add_argument('-rs', '--random_seed', type=float, choices=[Range(0.0,1.0)], default=None, help='Init with random seed: percent fill with 1s (very big/small most interesting)')
    args = parser.parse_args()

    init = 1
    pad = 1

    if args.demo:
        rule = 42
        iterations = 500
        kernel = np.array((
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]), dtype="int")
        grid = np.zeros((iterations, iterations*2+pad))
        center = math.floor((iterations*2+pad)/2)
        grid[math.floor(iterations/2)][center] = init
        framerate = 100
    else:                                                       # CHANGE THESE VALUES
        rule = int(args.rule)
        iterations = int(args.iterations)
        kernel = np.array((
            [1, 1, 0],
            [1, -1, 1],
            [0, 1, 1]), dtype="int")
        framerate = int(args.framerate)
        if args.random_seed:
            grid = np.random.choice(2,2*iterations**2, p=[1-args.random_seed,args.random_seed]).reshape(iterations,2*iterations).astype(float)
        else:
            grid = np.zeros((iterations, iterations*2+pad))
            center = math.floor((iterations*2+pad)/2)
            grid[math.floor(iterations/2)][center] = init

    binary_rule = np.flip([rule >> i & 1 for i in range(7,-1,-1)])
    # binary_rule = np.logical_not(binary_rule).astype(int)

    print("---------")
    print("Binary Rule: %s" % binary_rule)
    print("Kernel:\n%s" % kernel)
    if binary_rule[np.sum(kernel)] == 0 and binary_rule[0] == 1:
        flag = input("SEIZURE WARNING! Proceed? (y/n): ")
        if flag not in 'yY':
            print("Leaving program")
            quit()
    print("---------")

    s = time.time()
    while True:
        grid_correlated = cv2.filter2D(grid, -1, kernel).astype(int)
        grid = binary_rule[grid_correlated].astype(float)
        #grid_show = cv2.resize(grid, width=540, interpolation = cv2.INTER_NEAREST) 
        grid_show = imutils.resize(grid,width=1000)
        cv2.imshow("img",grid_show)
        cv2.waitKey(int(1/framerate * 1000)) #ms
        e = time.time()
        print('Framerate: %i FPS\r'%(1.0/(e-s)), end="")
        s = time.time()
