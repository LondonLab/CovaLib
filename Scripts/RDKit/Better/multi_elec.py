import random
import sys
from rdkit import Chem
from rdkit.Chem import rdChemReactions
from rdkit.Chem import AllChem

def main(name, argv):
    if len(argv) != 3:
        print_usage(name)
        return

    with open(argv[0], 'r') as f:
        reactions = [line.split() for line in f.readlines()]
    rxns = [[rdChemReactions.ReactionFromSmarts(r[0]), r[1]] for r in reactions]

    #read molport building blocks
    with open(argv[1], 'r') as f:
        lines_1 = [line.split() for line in f.readlines()]

    #creating RDKit Mol objects
    molecules_1 = list(map(lambda line: [Chem.MolFromSmiles(line[0]), line[1]], lines_1))
    molecules_1 = [m for m in molecules_1 if m[0] is not None]

    f = open(argv[2], 'w')
    # calculate reactions
    for i, rxn in enumerate(rxns):
        #find all valid molecules for a specific reaction
        reactents_smarts = rxn[0].GetReactants()
        has_patt_1 = list(map(lambda m: m[0].HasSubstructMatch(reactents_smarts[0]), molecules_1))
        reactent_option_1 = [m for i,m in enumerate(molecules_1) if has_patt_1[i]]
        print len(reactent_option_1)

        for mol1 in reactent_option_1:
            #calculate the product for the reaction for these two compounds
            products = rxn[0].RunReactants((mol1[0],))
            # write to file
            for i, pro in enumerate(products):
                f.write('%s\t%s_%s_%s\n' % (Chem.MolToSmiles(pro[0]), mol1[1], rxn[1], str(i+1)))
    f.close()

def print_usage(name):
    print "Usage : " + name + " <reactions> <library> <output>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
