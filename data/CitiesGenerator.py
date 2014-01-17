# coding: latin-1

"""

A quick-and-dirty script for generating travelling salesman problem.

Usage: generate_cities <number> <file>

Will generate <number> couple of numbers and put it in the format <file>
city1 x1 y2
city2 x2 y2
...

/!\ If <file> exists it will be overwritten.

""" 


import sys
from random import randint

MAX_X = MAX_Y = 500

try:
    filename = sys.argv[2]
    nb = int(sys.argv[1])
except:
    print (__doc__)
    sys.exit(1)

f = open(filename, "w")

for i in range(nb):
    line = "v%d %d %d\n" % (i, randint(0,MAX_X), randint(0,MAX_Y))
    f.write(line)

f.close()