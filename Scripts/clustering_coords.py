import os
import numpy
import sys
sys.path.append(os.environ["COVALIB"])
from Code import *
from rdkit import DataStructs
from rdkit import Chem
from rdkit.Chem.Fingerprints import FingerprintMols

rmsd_treshold = 1.2#2.0
coverage_treshold = 0.8#0.8
tanimoto_treshold = 0.85#0.7#0.5

def finger_print(smiles):
	return FingerprintMols.FingerprintMol(Chem.MolFromSmiles(smiles))

def tanimoto(fp1, fp2):
	return DataStructs.FingerprintSimilarity(fp1, fp2)

def main(name, argv):
        if not len(argv) == 1:
                print_usage(name)
                return

	poses = Poses_List.Poses_List(argv[0])
	cluster_rep = [0]
	cluster_fps = [finger_print(poses[0].get_smiles())]
	clusters = [[0]]
	for i, p in enumerate(poses[1:], start = 1):
		heavy_atoms = [atom for atom in p if not atom.get_atom() == 'H']
		fp = finger_print(p.get_smiles())
		clustered = False
		for j, clu in enumerate(cluster_rep):
			if tanimoto(fp, cluster_fps[j]) < tanimoto_treshold:
				continue
			counter = 0
			for p_atom in heavy_atoms:
				if min([numpy.linalg.norm(atom.get_coords() - p_atom.get_coords()) for atom in poses[clu] if atom.get_atom() == p_atom.get_atom()] + [rmsd_treshold]) < rmsd_treshold:
					counter += 1
			if 1.0 * counter / len(heavy_atoms) > coverage_treshold:
				clusters[j].append(i)
				clustered = True
				break
		if not clustered:
			cluster_rep.append(i)
			cluster_fps.append(fp)
			clusters.append([i])
        clusters.sort(key=len, reverse=True)
	os.mkdir('clusters')
	for i, clu in enumerate(clusters):
		poses.print_poses(clu, 'clusters/' + str(i) + '.mol2')

def print_usage(name):
        print "Usage : " + name + " <poses>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

