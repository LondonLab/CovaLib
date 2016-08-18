#Written by Daniel Zaidman
#Code review by 
import shutil
import subprocess
import os
import Paths
import PyUtils

class Mol2Utils:
    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.intro = []
        self.atom = []
        self.atom_names = []
        self.bond = []
    def process(self):
        '''while True:
            line = self.f.readline()
            if not line[0] == '#':
                break
        for i in range(6):
            self.intro.append(self.f.readline())'''
        while True:
            line = self.f.readline()
            self.intro.append(line)
            if '@<TRIPOS>ATOM' in line:
                break
        line = 'aaaaaaaaaaaaaaaa'
        while True:
            line = self.f.readline()
            if line[9] == 'B':
                break
            self.atom.append(line)
        self.bond.append(line)
        tmp_bond = self.f.readlines()
        for b in tmp_bond:
            if b[0] == '#':
                break
            self.bond.append(b)
        for atom in self.atom:
            self.atom_names.append(atom[8:11])
    def switch_names(self, atom_names):
        #self.atom_names = atom_names
        #for atom,name in zip(self.atom, self.atom_names):
        #    atom = atom[:8] + name + atom[11:]
        for i in range(len(atom_names)):
            self.atom[i] = atom_names[i] + self.atom[i][11:]
        self.atom = self.atom[:len(atom_names)]
        tmp = []
        for atom in self.atom:
            tmp.append([atom, atom[5:7]])
        sorted_list = sorted(tmp, key=lambda x:x[1])
        tmp = []
        for atom in sorted_list:
            tmp.append(atom[0])
        self.atom = tmp
        #self.atom = tmp
        #print self.atom
    def write_to_file(self, filename):
        self.all = [self.intro, self.atom, self.bond]
        with open(filename, 'w') as fout:
            for arr in self.all:
                for line in arr:
                    fout.write(line)
    def get_atom_names(self):
        return self.atom_names
    def get_intro(self):
        return self.intro
    def get_bond(self):
        return self.bond
    def set_intro(self, intro):
        self.intro = intro
    def set_bond(self, bond):
        self.bond = bond
    def close(self):
        self.f.close()
#Inner functions
    def delete_lines(self, lines, arr):
        for line in lines:
            arr.remove(line)
