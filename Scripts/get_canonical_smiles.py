from openeye.oechem import *
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
        if(len(argv) < 1 or len(argv) > 2 ):
            print_usage(name)
            return
        smiles = SMIUtil.get_canonical_smiles(argv[0])
	if len(argv) == 2 and (argv[1] == "p" or argv[1] == "P"):
		print smiles
	else:
		return smiles
                

def print_usage(name):
        print "Usage : " + name + " <smiles string>  [<P - to print result>]"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
