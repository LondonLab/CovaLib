import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
#sys.path.append('{0}/CovaLib'.format(os.environ['HOME']))
from Code import *


def main(name, argv):
    """
    Gets a folder containing the output of Prepare_Benchmark.py script for a single receptor and a 
    single ligand and runs the preparation steps and docking
    """
    if(len(argv) != 1):
        print_usage(name)
        return
    path = argv[0]
    rb = Benchmark.Benchmark(path)
    rb.Create_DB2_file()                        
    #rb.Create_DB2_file_crys()
    #rb.Prepare_Receptor() 
    rb.run_docking()
    rb.post_dock()
        
def print_usage(name):
        print "Usage : " + name + " <directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
