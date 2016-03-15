#Written by Daniel Zaidman
#Code review by 

import os
import subprocess
import sys
import numpy as np
import re
sys.path.append("/home/labs/londonir/danielza/CovaLib")
from Code import *
from subprocess import Popen, PIPE, STDOUT

def main(name, argv):
	if (not len(argv) == 3):
		print_usage(name)
		return
	dirlist = argv[0]
	#Run multiple Fpdock via cluster
	cluster = Cluster.Cluster("CHEM")
	cluster.runJobsName(dirlist, "python " + Paths.SCRIPTS + "SingleFpdock.py " + os.path.abspath(argv[1]) + " " + os.path.abspath(argv[2]))

def print_usage(name):
	print "Usage : " + name + " <sequences file> <start_pdb> <contraints_file>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
