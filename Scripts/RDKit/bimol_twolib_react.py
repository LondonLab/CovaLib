import random
import sys
from rdkit import Chem
from rdkit.Chem import rdChemReactions
from rdkit.Chem import AllChem

def main(name, argv):
    if len(argv) != 4:
        print_usage(name)
        return

    st = '[C;$(C[#6]);H1,$([CH0](-[#6])[#6]):1]=[OD1].[N;$(N[C,c]);!$(N=*);!$([N-]);!$(N#*);!$([ND3]);!$([ND4]);!$(NO);!$(N[C,S]=[S,O,N]):3]>>[C:1]-[N:3]'
#    rxns = [rdChemReactions.ReactionFromSmarts(argv[0])]
    rxns = [rdChemReactions.ReactionFromSmarts(st)]

    #read molport building blocks
    with open(argv[1], 'r') as f:
        lines_1 = [line.split() for line in f.readlines()]
    with open(argv[2], 'r') as f:
        lines_2 = [line.split() for line in f.readlines()]

    #creating RDKit Mol objects
    molecules_1 = list(map(lambda line: [Chem.MolFromSmiles(line[0]), line[1]], lines_1))
    molecules_1 = [m for m in molecules_1 if m[0] is not None]
    molecules_2 = list(map(lambda line: [Chem.MolFromSmiles(line[0]), line[1]], lines_2))
    molecules_2 = [m for m in molecules_2 if m[0] is not None]

    # calculate reactions
    for i, rxn in enumerate(rxns):
        #find all valid molecules for a specific reaction
        reactents_smarts = rxn.GetReactants()
        has_patt_1 = list(map(lambda m: m[0].HasSubstructMatch(reactents_smarts[0]), molecules_1))
        reactent_option_1 = [m for i,m in enumerate(molecules_1) if has_patt_1[i]]
        print len(reactent_option_1)
        has_patt_2 = list(map(lambda m: m[0].HasSubstructMatch(reactents_smarts[1]), molecules_2))
        reactent_option_2 = [m for i,m in enumerate(molecules_2) if has_patt_2[i]]
        print len(reactent_option_2)

    with open(argv[3], 'w') as file:
        for mol1 in reactent_option_1:
            for mol2 in reactent_option_2:
                #calculate the product for the reaction for these two compounds
                products = rxn.RunReactants((mol1[0], mol2[0]))
                # write to file
                file.write('%s\t%s_%s\n' % (Chem.MolToSmiles(products[0][0]), mol1[1], mol2[1]))

def print_usage(name):
    print "Usage : " + name + " <reaction_SMARTS> <library1> <library2> <output>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
