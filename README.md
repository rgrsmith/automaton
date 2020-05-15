Note: can edit kernel and grid manually to change evolution and initial conditions (eg probability distribution of (1,0) in grid or initial seed)


-rs should be a val between 0 and 1... argparse got a little gnarly


Cool Rules for center seed:
    ./automaton_animated.py -r 110 -f 100 -i 1000

    ./automaton_animated.py -r 222 -f 100 -i 1000 -rs .001


usage: automaton_animated.py [-h] [-r RULE] [-i ITERATIONS] [-f FRAMERATE]
                             [-d]
                             [-rs {<__main__.Range object at 0x7f70a0557ac8>}]

Generate Automatons

optional arguments:
  -h, --help            show this help message and exit
  -r RULE, --rule RULE  Choose a rule 0-255
  -i ITERATIONS, --iterations ITERATIONS
                        Number of iterations to run
  -f FRAMERATE, --framerate FRAMERATE
                        attempt to run at given framerate FPS
  -d, --demo            Run demo mode with preset pretty thing
  -rs {<__main__.Range object at 0x7f70a0557ac8>}, --random_seed {<__main__.Range object at 0x7f70a0557ac8>}
                        Init with random seed: percent fill with 1s (very
                        big/small most interesting)

