import sys
from rdkit import DataStructs
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Fingerprints import FingerprintMols
from sklearn.ensemble import RandomForestClassifier
import numpy
import os
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 1:
                print_usage(name)
                return

        with open(argv[0], 'r') as f:
            smiles = [Chem.MolFromSmiles(line.split()[0]) for line in f.readlines()]

        fps = [AllChem.GetMorganFingerprintAsBitVect(x,2,1024) for x in smiles]

        #convert the RDKit explicit vectors into numpy arrays
        np_fps = []
        for fp in fps:
            arr = numpy.zeros((1,))
            DataStructs.ConvertToNumpyArray(fp, arr)
            np_fps.append(arr)

        clusters=ClusterFps(fps,cutoff=0.4)
        for i, clu in enumerate(clusters):
            for c in clu:
                os.system('cat all/' + str(c + 1) + '.mol2 >> ' + 'clusters/' + str(i + 1) + '.mol2')

def print_usage(name):
        print "Usage : " + name + " <smile_file>"

def ClusterFps(fps,cutoff=0.2):
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

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
