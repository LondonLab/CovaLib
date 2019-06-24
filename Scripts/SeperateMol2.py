import subprocess
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
import itertools as it

def main(name, argv):
        if len(argv) == 0:
                print_usage(name)
                return
	PyUtils.create_folder('mols')

	i = -1
	with open(argv[0],'r') as f:
		for key,group in it.groupby(f,lambda line: line.startswith('@<TRIPOS>MOLECULE')):
			if key:
				i += 1
				mol = ''
				mol += ''.join(list(group))
			if not key:
				if not len(argv) == 1 and not str(i) in argv[1:]:
					continue
				mol += ''.join(list(group))
				with open('mols/' + str(i) + '.mol2', 'w') as f:
					f.write(mol)
	
def print_usage(name):
        print "Usage : " + name + " <poses file name> <index(s)>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
