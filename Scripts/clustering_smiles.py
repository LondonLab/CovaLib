import os
import numpy
import sys
sys.path.append(os.environ["COVALIB"])
from Code import *
from rdkit import DataStructs
from rdkit import Chem
from rdkit.Chem.Fingerprints import FingerprintMols

def ClusterFps(fps,cutoff=0.4):
    from rdkit import DataStructs
    from rdkit.ML.Cluster import Butina

    # first generate the distance matrix:                                                                                                    
    dists = []
    nfps = len(fps)
    for i in range(1,nfps):
        sims = DataStructs.BulkTanimotoSimilarity(fps[i],fps[:i])
        dists.extend([1-x for x in sims])

    # now cluster the data:                                                                                                                  
    cs = Butina.ClusterData(dists,nfps,cutoff,isDistData=True)
    return cs

def finger_print(smiles):
	return FingerprintMols.FingerprintMol(Chem.MolFromSmiles(smiles))

def tanimoto(fp1, fp2):
	return DataStructs.FingerprintSimilarity(fp1, fp2)

def main(name, argv):
        if not len(argv) == 1 and not len(argv) == 2:
                print_usage(name)
                return

        cutoff = 0.4
        if len(argv) == 2:
            cutoff = float(argv[1])

	with open(argv[0], 'r') as f:
            lines = f.readlines()
        smiles = [line.split()[0] for line in lines]

        molecules = list(map(lambda smile: [smile, Chem.MolFromSmiles(smile)], smiles))
        molecules = [m for m in molecules if m[1] is not None]

        fps = [finger_print(smile[0]) for smile in molecules]
	clusters = ClusterFps(fps,cutoff)
        os.mkdir('clusters')
        for i, clu in enumerate(clusters):
            with open('clusters/' + str(i) + '.smi', 'w') as f:
                for j in clu:
                    f.write(lines[j])
	
def print_usage(name):
        print "Usage : " + name + " <smiles> <cutoff (default = 0.4)>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

