import subprocess
import sys
import os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if len(argv) == 0:
                print_usage(name)
                return

	cluster = Cluster.Cluster()
	lines = []

	for pdb in open(argv[0], 'r'):
		#subprocess.call(["wget", "http://www.rcsb.org/pdb/files/" + pdb[:-1] + ".pdb"])
		lines.append("http://www.rcsb.org/pdb/files/" + pdb[:-1] + ".pdb")
	cluster.runCommandsArgs("wget", lines)

def print_usage(name):
        print "Usage : " + name + " <pdb_list_filename>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
