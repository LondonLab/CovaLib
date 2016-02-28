#Written by Daniel Zaidman
#Code review by 

import sys,os,math
sys.path.append("/home/labs/londonir/danielza/CovaLib")
from Code import *

def main(name, argv):
	if (len(argv) < 2 or len(argv) > 3):
		print_usage(name)
		return
	
	docking_job = DOCKovalent.DOCKovalent(*argv)

def print_usage(name):
	print "Usage : " + name + " <folder name> <compound> <library (default = False)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
