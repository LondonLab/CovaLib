import subprocess
import sys
import os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if len(argv) != 1:
                print_usage(name)
                return

	cluster = Cluster.Cluster()
	lines = []

	for line in open(argv[0], 'r'):
		#subprocess.call(["wget", "http://www.rcsb.org/pdb/files/" + pdb[:-1] + ".pdb"])
		lines.append(line[:-1])
	cluster.runCommands(lines)

def print_usage(name):
        print "Usage : " + name + " <job lines>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
