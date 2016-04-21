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
	if(len(argv) == 2):
		print rlist.findIndex(argv[1])
	elif(argv[2] == 'True'):
		print rlist.findIndexList(argv[1])
	
def print_usage(name):
	print "Usage : " + name + " <file_name> <zinc id> <list (default = false)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
