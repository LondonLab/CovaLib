#Written by Daniel Zaidman
#Code review by 

import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
	if not len(argv) == 4:
		print_usage(name)
		return
	smio = open(argv[2], 'w')
	with open(argv[0], 'r') as smi1:
		for line in smi1:
			min_tan = []
			with open(argv[1], 'r') as smi2:
				for line2 in smi2:
					tan = SMIUtil.tanimoto(line[:-1], line2[:-1], int(argv[3]))
					min_tan.append((tan, line2[:-1]))
			max_tan = max(min_tan)
			smio.write(max_tan[1] + ' ' + str(max_tan[0]) + '\n')
	smio.close()
	
def print_usage(name):
	print "Usage : " + name + " <ref smiles file> <fit smiles file> <out file> <FP type (0,1,2)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
