import numpy
import subprocess
import sys
import os
class Poses_List:
    def __init__(self, path, index = []):
        self.poses = []
	i = 0
	inside = False
        for line in open(path, 'r'):
		if not(inside) and line[0] == '#':
			i += 1
			inside = True
			if len(index) == 0 or str(i) in index:
				self.poses.append(pose())
                                cur_pose = self.poses[-1]
		if not line[0] == '#':
			inside = False
		if len(index) == 0 or str(i) in index:
			cur_pose.append(line)
                        if 'SMILE' in line:
                            cur_pose.set_smiles(line.split()[-1])
        for p in self.poses:
            p.arrange_coords()

    def __len__(self):
        return len(self.poses)
    def __getitem__(self, num):
        return self.poses[num]
    def print_poses(self, index, file_name):
        with open(file_name, 'w') as f:
            for i in index:
                for line in self.poses[i].get_text():
                    f.write(line)

class pose:
    def __init__(self):
        self.text = []
        self.atoms = []
    def append(self, line):
        self.text.append(line)
    def arrange_coords(self):
        self.coords = [line.split()[1:6] for line in self.text if len(line.split()) == 9]                
        self.coords = [[line[0], numpy.array((float(line[1]), float(line[2]), float(line[3]))), line[4].split('.')[0]] for line in self.coords]
        self.atoms = [atom(line) for line in self.coords]
    def get_coords(self):
        return self.coords
    def get_text(self):
        return self.text
    def __getitem__(self, i):
        return self.atoms[i]
    def set_smiles(self, smile):
        self.smile = smile
    def get_smiles(self):
        return self.smile

class atom:
    def __init__(self, line):
        self.atom_id = line[2]
        self.atom_name = line[0]
        self.coords = line[1]
        self.line = line
    def get_atom(self):
        return self.atom_id
    def get_coords(self):
        return self.coords
    def get_line(self):
        return self.line
