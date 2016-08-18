import subprocess
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
        if(len(argv) == 0):
                print_usage(name)
                return
        subprocess.call(["wget", "http://www.rcsb.org/pdb/files/" + argv[0] + ".pdb"])

def print_usage(name):
        print "Usage : " + name + " <pdb_name(s)>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
