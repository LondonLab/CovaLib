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
    def getName(self):
        return self.name

class Result_List:
    def __init__(self, file_name = None):
	self.res_list = []
        if(file_name == None):
            return
        f = open(file_name, 'r')
        for line in f:
            self.res_list.append(Compound(line.split()))
        f.close()
    def getList(self):
        return self.res_list
    def setList(self, nlist):
        self.res_list = nlist
    def sortList(self, fun):
        self.res_list = sorted(self.res_list, key = fun)
    def writeList(self, output, num = None):
        if(num == None):
            num = len(self.res_list)
        f = open(output, 'w')
        for c in self.res_list[:num]:
            f.write(str(c))
        f.close()
    def removeSubList(self, other, num):
        self.res_list = [x for x in self.res_list if x not in other.res_list[:num]]
    def findIndex(self, name):
        comp = Compound([0,0,name,0,0,0,0,0,0,0,0,0,0,0,0])
        if(comp not in self.res_list):
            return -1
        return self.res_list.index(comp) + 1
    def findIndexList(self, namelist):
        namearr = []
        for name in open(namelist, 'r'):
            namearr.append(self.findIndex(name[:-1]))
        return namearr
    def findZinc(self, index):
        return self.res_list[int(index) - 1].getName()
    def findZincList(self, indexlist):
        indarr = []
        for ind in open(indexlist, 'r'):
            indarr.append(self.findZinc(ind[:-1]))
        return indarr
    def writeIndexList(self, indexlist, output):
        newList = Result_List()
        arr = []
        for ind in open(indexlist, 'r'):
            arr.append(self.res_list[int(ind) - 1])
        newList.setList(arr)
        newList.writeList(output)
