#Written by Daniel Zaidman
#Code review by 

import sys,os,math
sys.path.append("/home/labs/londonir/danielza/CovaLib")
from Code import *

def main(name, argv):
	if (len(argv) != 5):
		print_usage(name)
		return
	
	prepare_job = DOCK_Prepare.DOCK_Prepare(*argv)
	prepare_job.blaster()
	prepare_job.changeIndock()

def print_usage(name):
	print "Usage : " + name + " <receptor> <ligand> <covalent_residue> <covalent_index> <atom_to_remove>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
