import sys
import os
#import Paths
import matplotlib.pyplot as plt
from pprint import pprint
import subprocess as sp
import Bio.PDB as bp
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import PDBUtils
from Code import Benchmark_Analyzer 

def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]
        ab = Benchmark_Analyzer.Analyzer(path)
        ab.create_base()
        ab.plot_hist_rmsd()
        #ab.create_scores()
        #ab.create_running_time()
        ab.plot_diff()
        #ab.plot_rotbonds_rmsd()

def print_usage(name):
        print "Usage : " + name + " <Run_directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
