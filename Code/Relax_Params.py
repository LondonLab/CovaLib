#Written by Daniel Zaidman
#Code review by 
import shutil
import subprocess
import os
import Paths
import PyUtils

class Relax_Params:
    def __init__(self, filename, c_index):
        self.f = open(filename, 'r')
        self.c_name = "C" + c_index
        if len(self.c_name) == 2:
            self.c_name += ' '
        self.Hs = []
        self.con_atoms = []
        self.intro = []
        self.atom = []
        self.bond = []
        self.chi = []
        self.nbr = []
        self.icoor = []
        self.connect = []
        self.rotamers = []
        self.parents = []
        self.all = [self.intro, self.atom, self.bond, self.chi, self.connect, self.nbr, self.icoor, self.rotamers]
    def get_con_atoms(self):
        return self.con_atoms
    def process(self):
        for i in range(4):
            self.intro.append(self.f.readline())
        for line in self.f:
            if line[:4] == 'ATOM':
                self.atom.append(line)
            if line[:4] == 'BOND':
                self.bond.append(line)
            if line[:3] == 'CHI':
                self.chi.append(line)
            if line[:3] == 'NBR':
                self.nbr.append(line)
            if line[:5] == 'ICOOR':
                self.icoor.append(line)
            if line[:3] == 'PDB':
                self.rotamers.append(line)
    def add_connect(self):
        self.connect.append("CONNECT " + self.c_name + '\n')
    def find_Hs(self):
        con_atom = ""
        lines_to_del = []
        for bond in self.bond:
            if self.c_name + " " in bond[11:]:
                if self.c_name in bond[11:14]:
                    con_atom = bond[16:19]
                else:
                    con_atom = bond[11:14]
                if con_atom[0] == 'H':
                    self.Hs.append(con_atom)
                    lines_to_del.append(bond)
                else:
                    self.con_atoms.append(con_atom)
        self.delete_lines(lines_to_del, self.bond)
    def find_parent(self):
        for bond in self.bond:
            sbond = bond[11:14] + bond[16:19]
            for con in self.con_atoms:
                if con in bond:
                    if not 'H' in sbond and not self.c_name in sbond:
                        if con in sbond[:3]:
                            self.parents.append(sbond[3:])
                        else:
                            self.parents.append(sbond[:3])
                        break
    def add_icoor(self):
        for i in range(len(self.con_atoms)):
            self.icoor.append("ICOOR_INTERNAL    CONN1 118.658581   67.565298    1.800000   " + self.c_name + "   " + self.con_atoms[i] + "   " + self.parents[i] + '\n')
    def delete_atoms(self):
        lines_to_del = []
        for line in self.atom:
            for H in self.Hs:
                if H in line[6:9]:
                    lines_to_del.append(line)
                    break
        self.delete_lines(lines_to_del, self.atom)
    def delete_icoor(self):
        lines_to_del = []
        for line in self.icoor:
            for H in self.Hs:
                if H in line[18:21]:
                    lines_to_del.append(line)
                    break
        self.delete_lines(lines_to_del, self.icoor)
    def write_to_file(self, filename):
        with open(filename, 'w') as fout:
            for arr in self.all:
                for line in arr:
                    fout.write(line)
    def close(self):
        self.f.close()
#Inner functions
    def delete_lines(self, lines, arr):
        for line in lines:
            arr.remove(line)
