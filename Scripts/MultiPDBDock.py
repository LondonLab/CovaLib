#input: pdbID_list,covalent_residue,covalent_index,atom_to_remove, folder_of_mol2_files
import sys,os
sys.path.append("/home/labs/londonir/danielza/CovaLib")
from Code import *
import subprocess
def main(name, argv):
        if (len(argv) != 1):
                print_usage(name)
                return
	#create a folder for each pdbID
        PDB_list = open(os.getcwd()+'/'+argv[0],'r').readlines()
	for i in range(len(PDB_list)):
                PDBid = PDB_list[i].strip()
		PyUtils.create_folder(os.getcwd()+"/"+PDBid)
                os.chdir(PDBid)
                cmd = ["~/../scripts/pdbUtil/getPdb.pl"+" -id "+PDBid]
                subprocess.call(cmd,shell=True)
                os.chdir("..")

def print_usage(name):
        print "Usage : " + name + " <PDB_list_file>"


if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
