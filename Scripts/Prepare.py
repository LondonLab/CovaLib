#!/usr/local/python-2.7.11/bin/python
#Written by Daniel Zaidman
#Code review by 

import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
	if len(argv) != 5 and len(argv) != 6:
		print_usage(name)
		return
	
	prepare_job = DOCK_Prepare.DOCK_Prepare(*argv)
	prepare_job.blaster()
	prepare_job.changeIndock()

def print_usage(name):
	print "Usage : " + name + " <receptor> <ligand> <covalent_residue> <covalent_index> <atom_to_remove> <tarting (default=False)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
