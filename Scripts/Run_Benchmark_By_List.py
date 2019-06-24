import subprocess as sp
import re
import os
import sys
from pprint import pprint
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *


OUTPUT_DIRECTORY = "Run_list"


def single(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]
        rb = Benchmark.Benchmark(path)
        rb.run()                        



def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]       
        receptor_dirs = open(path, 'r').readlines()
        #os.mkdir(OUTPUT_DIRECTORY)
        #for i in receptor_dirs:
            #sp.call("cp -r  Preparation/{0} {1}/".format(i, OUTPUT_DIRECTORY),shell=True)
        
        command = 'python {0}Single_Run_Benchmark.py'.format(Paths.SCRIPTS)
        cluster = Cluster.Cluster()
        cluster.runCommandsArgs(command, receptor_dirs)
                

def print_usage(name):
        print "Usage : " + name + " <list>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
