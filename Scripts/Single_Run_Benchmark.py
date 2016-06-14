import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
#sys.path.append('{0}/CovaLib'.format(os.environ['HOME']))
from Code import *

OUTPUT_DIRECTORY = "Run"
COVALENT_LINES  =  "REMARK @@@ covalent residue " 

DOCKING_RUN = "Docking_run"


def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]
        rb = d_Benchmark.Benchmark(path)
        rb.run()                        

def print_usage(name):
        print "Usage : " + name + " <directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
