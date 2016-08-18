import sys,os,math
from os import path
from os import listdir
from os.path import isfile, join, abspath
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
import subprocess

def main(name, argv):
	if (len(argv) <> 2):
                print_usage(name)
                return
	mypath_aligned = argv[0]
	mypath_ref = argv[1]
	onlyfiles_aligned = [os.getcwd()+"/"+mypath_aligned + a for a in listdir(mypath_aligned) if isfile(join(mypath_aligned, a)) and a[-4:] == '.pdb']
	onlyfiles_ref = [os.getcwd()+"/"+mypath_ref + b for b in listdir(mypath_ref) if isfile(join(mypath_ref, b)) and b[-4:] == '.pdb']

	ouf = open("rmsd_matrix.txt", "w") 
	for fi in onlyfiles_ref:
		for fj in onlyfiles_aligned:
			if (fj.split("/")[-1][:5]  == fi.split("/")[-1][:5]) and (fj.split("/")[-1][18:23]  == fi.split("/")[-1][14:19]):
				out_rmsd = open("rmsd.txt", "w")
				subprocess.call([Paths.SCRIPTS + "/rmsd.py", "-ref", fi, "-in", fj, "-overlay", "false"],stdout=out_rmsd)
				inf = open("rmsd.txt", "r")
				line = inf.readline()
				line_rms = line.split()
				full_line = line_rms[0]+" "+fi.split("/")[-1][:5] +" "+ fi.split("/")[-1][14:19]
				ouf.write(full_line)
				ouf.write("\n")
				inf.close()
				out_rmsd.close()
	ouf.close()
		
	return()

def print_usage(name):
	print "Usage : " + name + "<Folder_aligned_model>  <Folder_reference>"

if __name__ == "__main__":
        main(sys.argv[0], sys.argv[1:])
