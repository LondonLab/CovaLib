#Written by Daniel Zaidman
#Code review by 

import shutil
import subprocess
import os
import Paths
import PyUtils
import sys

class Compound:
    def __init__(self, arr):
        self.arr = arr
        self.name = arr[2]
        self.heavy_atoms = int(arr[7])
        self.score = float(arr[-1])
    def __str__(self):
        line = self.arr[0] + ' '
        for a in self.arr[1:-1]:
            line += a + '\t'
        line += self.arr[-1] + '\n'
        return line
    def getRelScore(self):
        return self.score / self.heavy_atoms
    def __eq__(self, other):
        return self.name == other.name

class Result_List:
    def __init__(self, file_name):
	self.res_list = []
        f = open(file_name, 'r')
        for line in f:
            self.res_list.append(Compound(line.split()))
        f.close()
    def getList(self):
        return self.res_list
    def sortList(self, fun):
        self.res_list = sorted(self.res_list, key = fun)
    def writeList(self, output, num):
        f = open(output, 'w')
        for c in self.res_list[:num]:
            f.write(str(c))
        f.close()
    def removeSubList(self, other):
        self.res_list = [x for x in self.res_list if x not in other.res_list]
