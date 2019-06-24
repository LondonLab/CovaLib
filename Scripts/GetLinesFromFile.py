import subprocess
import sys
import os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if len(argv) != 3:
                print_usage(name)
                return

	with open(argv[0], 'r') as f_index:
		with open(argv[1], 'r')as f_target:
			with open(argv[2], 'w')as f_output:
				j = 0
				while True:
					index = f_index.readline()
					if not index:
						break
					i = int(index)
					while i != j:
						j += 1
						line = f_target.readline()
					f_output.write(line)

def print_usage(name):
        print "Usage : " + name + " <index_file> <target_file> <output_file>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
