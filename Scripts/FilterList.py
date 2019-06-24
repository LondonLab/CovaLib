#Written by Daniel Zaidman
#Code review by 

import subprocess
import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
	if not len(argv) == 3 and not len(argv) == 4:
		print_usage(name)
		return
	file_name = 'extract_all.sort.uniq.txt'
	folder_name = argv[2]
	if argv[0] == '1':
		function = Result_List.Compound.getRelScore
	if argv[0] == '2':
		function = Result_List.Compound.getSmallPolarity
	out_name = folder_name + '/' + file_name
	PyUtils.create_folder(folder_name)
        rlist = Result_List.Result_List(argv[1] + '/' + file_name)
        rlist.filterList(function)
        rlist.writeList(out_name, 500)
	if len(argv) == 4 and argv[3] == 'True':
		subprocess.call([Paths.DOCKBASE + "analysis/getposes.py", "-f", out_name, "--ranks", out_name, "-o", folder_name + "/poses.mol2"])

def print_usage(name):
	print "Usage : " + name + " <which filter (1 for Big molecules)> <input_extract_folder> <output_extract_folder> <extract poses (Default = False)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
