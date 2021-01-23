import random
import sys
from rdkit import Chem
from rdkit.Chem import rdChemReactions
from rdkit.Chem import AllChem

def main(name, argv):
    if len(argv) != 3:
        print_usage(name)
        return
    rxn = rdChemReactions.ReactionFromSmarts(argv[0])
    reactents_smarts = rxn.GetReactants()

    #read molport building blocks
    with open(argv[1], 'r') as f:
        lines = [line.split() for line in f.readlines()]

    with open(argv[2], 'w') as f:
        for line in lines:
        #creating RDKit Mol objects
            molecule = [Chem.MolFromSmiles(line[0]), line[1]]
            if molecule[0] is None:
                continue

        # calculate reactions
            if not molecule[0].HasSubstructMatch(reactents_smarts[0]):
                continue

        #calculate the product for the reaction for these two compounds
            products = rxn.RunReactants((molecule[0],))
        #write to file
            f.write('%s\t%s\n' % (Chem.MolToSmiles(products[0][0], True), molecule[1]))

def print_usage(name):
    print "Usage : " + name + " <reaction_SMARTS> <library> <output>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
