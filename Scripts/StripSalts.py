import subprocess
import sys
import os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 2:
                print_usage(name)
                return

	with open(argv[0], 'r') as f:
		lines = [line.split() for line in f.readlines()]
	for i in range(len(lines)):
		lines[i][0] = max(lines[i][0].split('.'), key=len)
	with open(argv[1], 'w') as f:
		for line in lines:
			f.write('\t'.join(line) + '\n')

def print_usage(name):
        print "Usage : " + name + " <smiles> <output>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
