import os
import numpy
import sys
sys.path.append(os.environ["COVALIB"])
from Code import *
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem import rdChemReactions
from rdkit.Chem import AllChem

def main(name, argv):
        if not len(argv) == 2:
                print_usage(name)
                return

	rxn = rdChemReactions.ReactionFromSmarts('[C:1][SiH3]>>[C:1]n1nnnn1')
	reactents_smarts = rxn.GetReactants()
	back = rdChemReactions.ReactionFromSmarts('[C:1]n1nnnn1>>[C:1][SiH3]')
	back_smarts = back.GetReactants()

	with open(argv[0], 'r') as f:
            lines = f.readlines()
        smiles = [line.split() for line in lines]

	with open(argv[1], 'w') as f:
		for line in smiles:
			mol = [Chem.MolFromSmiles(line[0]), line[0], line[1]]
			if mol is None:
				continue
			if not mol[0].HasSubstructMatch(reactents_smarts[0]):
				continue
			fake_ring = rxn.RunReactants((mol[0],))[0][0]
			fake_ring = Chem.MolFromSmiles(Chem.MolToSmiles(fake_ring))
			core = MurckoScaffold.GetScaffoldForMol(fake_ring)
			if core.HasSubstructMatch(back_smarts[0]):
				scaffold = back.RunReactants((core,))[0][0]
			else:
				scaffold = Chem.MolFromSmiles('O=C(N)C[SiH3]')
			f.write('%s\t%s\t%s\n' % (Chem.MolToSmiles(scaffold), line[0], line[1]))

def print_usage(name):
        print "Usage : " + name + " <smiles> <output>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

