#Written by Daniel Zaidman
#Code review by 

import subprocess
import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
	if not len(argv) == 1 and not len(argv) == 2:
		print_usage(name)
		return

	os.chdir(argv[0])
	subprocess.call([Paths.DOCKBASE + "analysis/extract_all.py", "--done"])
	if len(argv) == 1 or (len(argv) == 2 and argv[1] == 'True'):
		subprocess.call([Paths.DOCKBASE + "analysis/getposes.py", "-l", "1000"])

def print_usage(name):
	print "Usage : " + name + " <folder name> <extract poses (Default = True)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
