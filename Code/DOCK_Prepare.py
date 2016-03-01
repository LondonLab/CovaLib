#Written by Daniel Zaidman
#Code review by 

import shutil
import subprocess
import os
import Paths

class DOCK_Prepare:
    def __init__(self, rec, lig, cov, cov_index, HG):
        self.rec = rec
        self.lig = lig
	self.folder = os.path.dirname(os.path.realpath(rec)) + "/"
        self.fixed_rec = self.folder + "rec.pdb"
        self.fixed_lig = self.folder + "xtal-lig.pdb"
        self.cov = cov
        self.cov_index = cov_index
        self.hg = HG
    def blaster(self):
        self.create_fixed_names()
        subprocess.call([Paths.DOCKBASE + "proteins/blastermaster/blastermaster.py", "--covalentResNum", self.cov_index, "--covalentResName", self.cov, "--covalentResAtoms", self.hg])
    def changeIndock(self):
        INDOCK = self.folder + "INDOCK"
        old = open(INDOCK, 'r')
        new = open(INDOCK + '2', 'w')
        for i in range(17):
            line = old.readline()
            new.write(line)
        for i in range(2):
            line = old.readline()
            new.write(line[:-3] + "00.0\n")
        for i in range(24):
            line = old.readline()
            new.write(line)
        line = old.readline()
        new.write(line[:-3] + "yes\n")
        for line in old:
            new.write(line)
        old.close()
        new.close()
        os.remove(INDOCK)
        os.rename(INDOCK + '2', INDOCK)
#Inner functions
    def create_fixed_names(self):
        shutil.copyfile(self.rec, self.fixed_rec)
        shutil.copyfile(self.lig, self.fixed_lig)
