#Written by Daniel Zaidman
#Code review by 

import subprocess
import sys,os,math
sys.path.append("/home/labs/londonir/danielza/CovaLib")
from Code import *

def main(name, argv):
	if (not len(argv) == 1):
		print_usage(name)
		return
	
	combineResults(argv[0])

def print_usage(name):
	print "Usage : " + name + " <folder name> <compound> <library (default = False)>"

def combineResults(folder_name):
	os.chdir(folder_name)
        subprocess.call([Paths.DOCKBASE + "analysis/extract_all.py", "--done"])
        subprocess.call([Paths.DOCKBASE + "analysis/getposes.py"])

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
