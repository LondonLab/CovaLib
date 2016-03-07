#input: pdbID_list,covalent_residue,covalent_index,atom_to_remove, folder_of_mol2_files
import sys,os
sys.path.append("/home/labs/londonir/dinad/CovaLib")
from Code import *
def main(name, argv):
        if (len(argv) != 1):
                print_usage(name)
                return
#creates folder for each PDB and downloads .pdb for it
        PDBUtils.DownloadPDBs(argv[0])
        PDBUtils.rec(argv[0])
        PDBUtils.lig(argv[0])#user needs to choose ligand

def print_usage(name):
        print "Usage : " + name + " <PDB_list_file>"


if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
