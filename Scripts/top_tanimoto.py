import os
import numpy
import sys
sys.path.append(os.environ["COVALIB"])
from Code import *
from rdkit import DataStructs
from rdkit import Chem
from rdkit.Chem.Fingerprints import FingerprintMols

def finger_print(smiles):
	return FingerprintMols.FingerprintMol(Chem.MolFromSmiles(smiles))

def tanimoto(fp1, fp2):
	return DataStructs.FingerprintSimilarity(fp1, fp2)

def main(name, argv):
        if not len(argv) == 3:
                print_usage(name)
                return

        query = argv[0]
        cutoff = float(argv[2])

	with open(argv[1], 'r') as f:
            lines = f.readlines()
        smiles = [line.split()[0] for line in lines]
        top = []
        f_query = finger_print(query)
        for smile in smiles:
		score = tanimoto(f_query, finger_print(smile))
		if score > cutoff:
			top.append([smile, score])
	top.sort(reverse=True, key=lambda x: x[1])
        for t in top:
		print t[0]
	
def print_usage(name):
        print "Usage : " + name + " <smile> <database> <cutoff>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

