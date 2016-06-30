import subprocess as sp
import re
import os
import sys
from pprint import pprint
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

OUTPUT_DIRECTORY = "Run"


def main(name, argv):
    """
    Gets a folder containing folders for each one of the receptors with their output 
    of Prepare_Benchmark.py SCRIPTS and runs the preparation steps and docking for 
    one of the receptors.    
    """
    if(len(argv) != 1):
        print_usage(name)
        return

    path = argv[0]       
    receptor_dirs = []
    for subdir in os.listdir( path ):
        if not subdir.startswith('.'):
            receptor_dirs.append('/'.join([path, subdir]))

    command = 'python {0}Single_Run_Benchmark.py'.format(Paths.SCRIPTS)
    cluster = Cluster.Cluster()
    cluster.runCommandsArgs(command, receptor_dirs)
                

def print_usage(name):
        print "Usage : " + name + " <Preparation_directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
