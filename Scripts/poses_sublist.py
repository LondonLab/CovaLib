import os
import numpy
import sys
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if len(argv) < 3:
                print_usage(name)
                return

	if os.path.isfile(argv[2]):
		with open(argv[2], 'r') as f:
			indices = [line[:-1] for line in f]
	else:
		indices = [int(i) for i in argv[2:]]
	poses = Poses_List.Poses_List(argv[0], indices)
	poses.print_poses(range(len(indices)), argv[1])

def print_usage(name):
        print "Usage : " + name + " <poses> <outfile> <indices / filename>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

