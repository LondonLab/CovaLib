import sys
import os
import Paths
import matplotlib.pyplot as plt
from pprint import pprint
import subprocess as sp
import Bio.PDB as bp
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import PDBUtils




DOCKING_RUN_FILES = "Docking_run"
OUTPUT_FILE = ''


class Ligand_Dihedral(object):
    def __init__(self, pdb_path, summary_path):  
        """path - for a pdb file"""
        self.pdb_path = pdb_path 
        self.summary_path = summary_path
        self.current_location = os.getcwd()
        self.load_data()
        
    def load_data(self):
        #self.file = open(self.pdb_path, 'r').readlines()
        parser = bp.PDBParser()
        self.structure = parser.get_structure(self.receptor_name, self.pdb_path)
        summary = open(self.summary_path, 'r').read()
        self.summary = dict()


 
               
def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]
        ab = Analyze_Bechmark(path)


def print_usage(name):
        print "Usage : " + name + " <pdb_path>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

