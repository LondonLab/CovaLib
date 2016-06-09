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
        count = PDBUtils.count_heavy_atom(path)
        sp.call(['echo', 'there are ', str(count), ' heavy atoms'])
                

def print_usage(name):
        print "Usage : " + name + " <PDB_path>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
