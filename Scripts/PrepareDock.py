#Written by Daniel Zaidman                                                                                                                                                                                                                                                    
#Code review by                                                                                                                                                                                                                                                               

import sys,os,math
sys.path.append(os.environ["COVALIB"])
from Code import *
import subprocess
import shutil

def main(name, argv):
        if not len(argv) == 8:
                print_usage(name)
                return

        subprocess.call(['python', Paths.SCRIPTS + 'Prepare.py'] + argv[:5])
        subprocess.call(['python', Paths.SCRIPTS + 'DOCKovalentTask.py'] + argv[5:])

def print_usage(name):
        print "Usage : " + name + " <receptor> <ligand> <covalent_residue> <covalent_index> <atom_to_remove> <folder name> <compound> <library (default = False)>"

if __name__ == "__main__":
        main(sys.argv[0], sys.argv[1:])
