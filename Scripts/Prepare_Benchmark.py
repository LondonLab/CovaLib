import subprocess as sp
import sys
from pprint import pprint
import Bio.PDB as bp
import re
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
import math

OUTPUT_DIRECTORY = "Preparation"
DIHEDRAL_OUTPUT = 'dihedral'


def main(name, argv):
    """
    Creates all files needed for Preparering ligand & receptor in the list for docking.

    Files/Directories:
        OUTPUT_DIRECTORY - will contain a directory for each receptor and ots ligand
        error_prepare.txt - recetor + chain that didn't have a match in the summary file    
    """
    # Check input
    if(len(argv) != 2):
        print_usage(name)
        return

    # creates main directory of all receptors
    sp.call("mkdir {0}".format(OUTPUT_DIRECTORY), shell=True)
    
    # Reads pdb list & summary files
    list_pdbs = open(argv[0],'r').readlines()
    summary_file = open(argv[1], 'r').readlines()
    
        
    prev_name = '@@' #for counting 
    count = 1
    err_file = open('error_prepare.txt','w')
    # iterating through every receptor in list
    for line in list_pdbs:
        # Parsing the line of the pdb list: <PDB id><chain>
        name = line.split()[0]
        chain = line.split()[-1]
        print name
        print chain
        # Searches the matching line in the summary file
        pattern = "{0}\s+{1}".format(name, chain)
        line_summary = [i for i in summary_file if re.search(pattern, i) != None]
        # If one receptors have multiple ligads in PDB list file
        count = 1 if prev_name != name else count
        prev_name = name
        
        if len(line_summary) == 0:
            # if there is no lune in the summary file for the receptor 
            err_file.write(name + chain+ '\n')
                
        else: 
            # a receptor + chain can have multiple covalent residues in the summary file
            for cov_res in line_summary:
                # no data 
                if 'empty' in cov_res:
                    continue
                    
                # creatse a directory for this receptor inside the main directory 
                path = '{0}/{1}_{2}'.format(OUTPUT_DIRECTORY, name, str(count))
                sp.call('mkdir {0}'.format(path), shell=True)
                count +=1
                
                #Debug
                print '*'*70
                print name, chain,':'
                prep = Prepare_benchmark.Prepare(name, path, cov_res) 
                prep.run()
            

def print_usage(name):
        print "Usage : " + name + " <list_path>  <summary_path>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
