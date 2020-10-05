import sys, os
from rdkit import Chem

def main(name, argv):
    if len(argv) != 3:
        print_usage(name)
        return

    with open(argv[0], 'r') as f:
        lines = []
        for line in f:
            l = [Chem.MolFromSmiles(line.split()[0]), line.split()[1]]
            if not l[0] == None and len(l[0].GetSubstructMatches(Chem.MolFromSmarts(argv[1]))) == 1:
                lines.append(l)
    with open(argv[2], 'w') as f:
        for line in lines:
            f.write(Chem.MolToSmiles(line[0]) + '\t' + line[1] + '\n')

def print_usage(name):
    print "Usage : " + name + " <library> <substructure> <output file>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
