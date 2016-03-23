#Written by Daniel Zaidman
#Code review by 

import subprocess
import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
	if (not (len(argv) == 2 or len(argv) == 3)):
		print_usage(name)
		return
        rlist = Result_List.Result_List(argv[0])
        rlist.sortList(Result_List.Compound.getRelScore)
	if(len(argv) == 3):
	        nlist = Result_List.Result_List(argv[2])
		rlist.removeSubList(nlist, 500)
        rlist.writeList(argv[1], 500)
	
def print_usage(name):
	print "Usage : " + name + " <file_name> <output_name> <already checked file name - optional>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
