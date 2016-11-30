#Written by Daniel Zaidman                                                                                                                                                                                                                                                    
#Code review by                                                                                                                                                                                                                                                               

import sys,os,math
sys.path.append(os.environ["COVALIB"])
from Code import *
import subprocess
import shutil

def main(name, argv):
        if not len(argv) == 3 and not len(argv) == 2:
                print_usage(name)
                return

	if len(argv) == 3:
		argv[2] = float(argv[2])
        print ','.join(PDBUtils.expand(*argv))

def print_usage(name):
        print "Usage : " + name + " <ref> <selection> <dist (default=4.0)>"

if __name__ == "__main__":
        main(sys.argv[0], sys.argv[1:])
