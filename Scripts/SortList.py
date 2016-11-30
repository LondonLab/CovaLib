#Written by Daniel Zaidman
#Code review by 

import subprocess
import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
	if (not (len(argv) == 1 or len(argv) == 2)):
		print_usage(name)
		return
	file_name = 'extract_all.sort.uniq.txt'
	if argv[1] == '1':
		folder_name = 'big_molecules'
		function = Result_List.Compound.getBigMols
		out_name = folder_name + '/extract_all.big.txt'
	PyUtils.create_folder(folder_name)
        rlist = Result_List.Result_List(file_name)
        rlist.sortList(function, folder_name + '/eff_score.txt', int(argv[0]))
	'''if(len(argv) == 4):
	        nlist = Result_List.Result_List(argv[1])
		rlist.removeSubList(nlist, 500)'''
        rlist.writeList(out_name, int(argv[0]))
	subprocess.call([Paths.DOCKBASE + "analysis/getposes.py", "-f", out_name, "--ranks", out_name, "-o", folder_name + "/poses.mol2"])

def print_usage(name):
	print "Usage : " + name + " <number> <which filter (1 for Big molecules)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
