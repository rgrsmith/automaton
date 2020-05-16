#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import argparse
import math
import cv2
import imutils
from gui import GUI

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
    
    gui = GUI(args.__dict__)
    gui.update_gui()

    def reset_init():
        global gui
        if gui.params['demo']:
            gui.params['rule'] = 42
            gui.params['iterations'] = 500
            gui.params['kernel'] = np.array((
                [0, 1, 0],
                [1, 0, 1],
                [0, 1, 0]), dtype="int")
            gui.params['grid'] = np.zeros((gui.params['iterations'], gui.params['iterations']*2+pad))
            center = math.floor((gui.params['iterations']*2+pad)/2)
            gui.params['grid'][math.floor(gui.params['iterations']/2)][center] = init
            gui.params['framerate'] = 100
        else:                                                       # CHANGE THESE VALUES
            gui.params['kernel'] = np.array((
                [1, 1, 0],
                [1, -1, 1],
                [0, 1, 1]), dtype="int")
            gui.params['framerate'] = int(args.framerate)
            if gui.params['random_seed']:
                prob_1 = gui.params['random_seed']
                gui.params['grid'] = np.random.choice(2,2*gui.params['iterations']**2, p=[1-prob_1,prob_1]).reshape(gui.params['iterations'],2*gui.params['iterations']).astype(float)
            else:
                gui.params['grid'] = np.zeros((gui.params['iterations'], gui.params['iterations']*2+pad))
                center = math.floor((gui.params['iterations']*2+pad)/2)
                gui.params['grid'][math.floor(gui.params['iterations']/2)][center] = init

        gui.params['binary_rule'] = np.flip([gui.params['rule'] >> i & 1 for i in range(7,-1,-1)])
        # binary_rule = np.logical_not(binary_rule).astype(int)

        gui.params['reset'] = False

    reset_init()

    print("---------")
    print("Binary Rule: %s" % gui.params['binary_rule'])
    print("Kernel:\n%s" % gui.params['kernel'])
    if gui.params['binary_rule'][np.sum(gui.params['kernel'])] == 0 and gui.params['binary_rule'][0] == 1:
        flag = input("SEIZURE WARNING! Proceed? (y/n): ")
        if flag not in 'yY':
            print("Leaving program")
            quit()
    print("---------")

    s = time.time()
    while True:
        grid_correlated = cv2.filter2D(gui.params['grid'], -1, gui.params['kernel']).astype(int)
        gui.params['grid'] = gui.params['binary_rule'][grid_correlated].astype(float)
        #grid_show = cv2.resize(grid, width=540, interpolation = cv2.INTER_NEAREST) 
        grid_show = imutils.resize(gui.params['grid'],width=1000)
        cv2.imshow("img",grid_show)
        cv2.waitKey(int(1/gui.params['framerate'] * 1000)) #ms
        gui.update_gui()
        if gui.params['reset']:
            reset_init()
            gui.params['demo'] = False
        e = time.time()
        print('Framerate: %i FPS\r'%(1.0/(e-s)), end="")
        s = time.time()
