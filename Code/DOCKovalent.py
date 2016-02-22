import shutil
import subprocess

def hello_world():
	print "hello world"

class DOCKovalent:
    def __init__(self, folder, rec, lig, cov, cov_index, library = None):
        self.folder = folder
        self.rec = folder + rec
        self.lig = folder + lig
        self.fixed_rec = folder + "rec.pdb"
        self.fixed_lig = folder + "xtal-lig.pdb"
        self.cov = cov
        self.cov_index = cov_index
        self.hg = self.find_hg()
        self.library = library
    def blaster(self):
        self.create_fixed_names()
        subprocess.call(["$DOCKBASE/proteins/blastermaster/blastermaster.py", "--covalentResNum", self.cov_index, "--covalentResName", self.cov, "--covalentResAtoms", self.hg])

#Inner functions
    def find_hg(self):
        if(cov == CYS):
            return 'HG'
        return 'HG1'
    def create_fixed_names(self):
        shutil.copyfile(self.rec, self.fixed_rec)
        shutil.copyfile(self.lig, self.fixed_lig)
