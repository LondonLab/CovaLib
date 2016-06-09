import subprocess as sp
import re
import os
import sys
from pprint import pprint
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

OUTPUT_DIRECTORY = "Run"


def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]       
        #sp.call("cp -r {0} {1}".format(path, OUTPUT_DIRECTORY),shell=True)
        receptor_dirs = []
        for subdir in os.listdir( path ):
            if not subdir.startswith('.'):
                receptor_dirs.append('/'.join([path, subdir]))
        #for subdir, dirs, files in os.walk(OUTPUT_DIRECTORY):
            #if files != []:
                #receptor_dirs.append(subdir)
        command = 'python {0}Single_Run_Benchmark.py'.format(Paths.SCRIPTS)
        cluster = Cluster.Cluster()
        cluster.runCommandsArgs(command, receptor_dirs)
                

def print_usage(name):
        print "Usage : " + name + " <Preparation_directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
