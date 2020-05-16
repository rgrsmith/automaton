Note: can edit kernel and grid manually to change evolution and initial conditions (eg probability distribution of (1,0) in grid or initial seed)

Seizure warning will print, followed by short delay, if the background will quickly oscillate black/white (not guaranteed to cover all cases)

-rs should be a val between 0 and 1... argparse got a little gnarly


Cool Rules for center seed and this kernel:
Kernel:
[[0 1 0]
 [1 0 1]
 [0 1 0]]
---------
    ./automaton_animated.py -r 110 -f 100 -i 1000
    ./automaton_animated.py -r 222 -f 100 -i 1000 -rs .001



./automaton_animated.py -r 230 -f 100 -i 1000
---------
Binary Rule: [0 1 1 0 0 1 1 1]
Kernel:
[[ 1  1 -3]
 [ 1 -1  1]
 [-3  1  1]]
---------



cooll other rules:
./automaton_animated.py -r 30 -f 100 -i 1000 -rs .99999
---------
Binary Rule: [0 1 1 1 1 0 0 0]
Kernel:
[[ 1  1  0]
 [ 1 -1  1]
 [ 0  1  1]]
---------

- the above kernel with 33, 36, 40, 100 (with very high -rs), 100 (with rs of .01 = twinkly sky), 231 (rs .01) = crystallines,

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

