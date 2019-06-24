import subprocess
import sys
import os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 2:
                print_usage(name)
                return
	input_ter = argv[0].split('.')[-1]
	output_ter = argv[1].split('.')[-1]
	subprocess.call(["/work/londonlab/software/openbabel-2.3.2/bin/obabel", "-i", input_ter, argv[0], "-o", output_ter, "-O", argv[1]])

def print_usage(name):
        print "Usage : " + name + " <in_file> <out_file>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
