import random
import sys
from rdkit import Chem
from rdkit.Chem import rdChemReactions
from rdkit.Chem import AllChem

def main(name, argv):
    if len(argv) != 3:
        print_usage(name)
        return
    rxns = [rdChemReactions.ReactionFromSmarts(argv[0])]
    
    #read molport building blocks
    with open(argv[1], 'r') as f:
        lines = [line.split() for line in f.readlines()]

    #creating RDKit Mol objects
    molecules = list(map(lambda line: [Chem.MolFromSmiles(line[0]), line[1]], lines))
    molecules = [m for m in molecules if m[0] is not None]

    # calculate reactions
    for i, rxn in enumerate(rxns):
        #find all valid molecules for a specific reaction
        reactents_smarts = rxn.GetReactants()
        has_patt_1 = list(map(lambda m: m[0].HasSubstructMatch(reactents_smarts[0]), molecules))
        reactent_option_1 = [m for i,m in enumerate(molecules) if has_patt_1[i]]
        print len(reactent_option_1)

    with open(argv[2], 'w') as file:
        for mol1 in reactent_option_1:
            #calculate the product for the reaction for these two compounds
            products = rxn.RunReactants((mol1[0],))
            #write to file
            file.write('%s\t%s\n' % (Chem.MolToSmiles(products[0][0]), mol1[1]))

def print_usage(name):
    print "Usage : " + name + " <reaction_SMARTS> <library> <output>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
