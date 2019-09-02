import os
import numpy
import sys
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 3:
                print_usage(name)
                return

	poses = Poses_List.Poses_List(argv[2])

        with open(argv[0], 'r') as f:
            atoms = [line.split()[1:6] for line in f if len(line.split()) == 9]
	for atom in atoms:
		atom[-1] = atom[-1].split('.')[0]
        with open(argv[1], 'r')as f:
            queries = [line.split() for line in f]
	queries_atoms = []
	for q in queries:
		for line in atoms:
			if line[0] == q[0]:
				queries_atoms.append([line[-1], numpy.array((float(line[1]), float(line[2]), float(line[3]))), float(q[1])])

	indices = []
	for i, p in enumerate(poses):
		is_ok = True
		for query in queries_atoms:
			#if len([atom for atom in p if atom.get_atom() == query[0] and numpy.linalg.norm(query[1] - atom.get_coords()) <= query[2]]) == 0:
                        if len([atom for atom in p if atom.get_atom() in ['N', 'O'] and numpy.linalg.norm(query[1] - atom.get_coords()) <= query[2]]) == 0:
				is_ok = False
				break
		if is_ok:
			indices.append(i)
	poses.print_poses(indices, 'filtered.mol2')

def print_usage(name):
        print "Usage : " + name + " <xtal-lig (.mol2)> <file with atom names and tresholds> <poses>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

