import random
import sys
from rdkit import Chem
from rdkit.Chem import rdChemReactions
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors

def main(name, argv):
    if len(argv) != 3:
        print_usage(name)
        return
    
    MW = float(argv[1])
    RB = int(argv[2])

    #read molport building blocks
    with open(argv[0], 'r') as f:
        for line in f:
            line_s = line.split()
            molecule = [Chem.MolFromSmiles(line_s[0]), line_s[1]]
            if molecule[0] == None:
                continue
            if Descriptors.MolWt(molecule[0]) <= MW and rdMolDescriptors.CalcNumRotatableBonds(molecule[0]) <= RB:
                print Chem.MolToSmiles(molecule[0]) + "\t" + line_s[1]
                #print line_s[0] + "\t" + line_s[1]
#            else:
#                print Descriptors.MolWt(molecule[0]) <= MW
#                print rdMolDescriptors.CalcNumRotatableBonds(molecule[0])

def print_usage(name):
    print "Usage : " + name + " <library> <max MW> <max rotational bonds>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
