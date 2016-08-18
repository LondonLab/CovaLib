import subprocess
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
        if not len(argv) == 4:
                print_usage(name)
                return
        ros_sc = RosettaScore.RosettaScore(int(argv[0]))
	ros_sc.tarBest(int(argv[1]), argv[2], argv[3])

def print_usage(name):
        print "Usage : " + name + " <runs> <number of best scores> <prefix of result files> <out tar file>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
