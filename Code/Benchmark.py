import subprocess as sp
import sys
from pprint import pprint
import Bio.PDB as bp
import re
import os
import Paths
import DOCKovalent


class Benchmark(object):
    """
    This class can run the different steps of the docking:
        1. Prepare ligand
        2. prepare receptor
        3. Docking
        4. combine results and get rmsd of pose to x-ray 
        
    Assumes files for every receptor were ptrepared with Prepare_benchmark.py script!!
    """
    
    def __init__(self, path):
        """
        initializes:
            receptor_name
            path - to the receptor's directory
            COVALENT_LINES - template for rec.pdb lines having info from the summary file
            DOCKING_RUN - directory for docking output's files
            receptor - see function _initialize_prep_files
            file - see function _initialize_prep_files
            ligand_dict - see function _initialize_prep_files
            covalent_res - see function _initialize_prep_files
            covalent_atom_dict - the covalent atom of each residue
            current_location
        """
        
        #initializing:
        ind = path.rfind("/") 
        self.receptor_name = path[ind+1 : ind+5] # the foleder's name is XXXX or XXXX_n where XXXX is the pdb code
        
        # debug
        print '#'*60
        print '#'*10, self.receptor_name
        print '#'*60
        
        
        self.path = os.path.abspath(path) # path to the current receptor's folder (usually in the Run folder)
        self.COVALENT_LINES = "REMARK @@@ covalent residue " 
        self.DOCKING_RUN = "Docking_run"
        self._initialize_prep_files()
        
        # for preparint the receptor
        self.covalent_atom_dict = {'CYS':'HG', 'THR':'HG1'}
        self.current_location = os.getcwd()
        
    def _initialize_prep_files(self):
        """
        init:
            receptor - Bio PDB structure of the receptor
            file - receptor PDB as a strings list
            ligand_dict - a dictionary saving the name and chain of the ligand
            covalent_res - Bio PDB residue object of the receptor's covalent residue
        """
        
        # get receptor structure as object & list
        parser = bp.PDBParser()
        rec_file = "{0}/rec.pdb".format(self.path)
        self.receptor = parser.get_structure(self.receptor_name, rec_file)
        self.file = open(rec_file ,'r').readlines()
        
        # get summary info saved in recveptor's PDB remarks
        covalent_lines = [line for line in self.file if line.startswith(self.COVALENT_LINES )]
        self.ligand_dict = dict()
        for line in covalent_lines:
            if " id " in line:
                covnum = line.split()[-1]
            elif " chain " in line:
                cov_chain = line.split()[-1] 
            elif "lig_name" in line:
                self.ligand_dict['name'] = line.split()[-1] 
            elif "lig_chain" in line:
                self.ligand_dict['chain'] = line.split()[-1]
        self.covalent_res = self.receptor[0][cov_chain][int(covnum)]   

    def run(self):
        """Deprecated!!"""
        self.Create_DB2_file()
        self.Create_DB2_file_crys()
       
        self.Prepare_Receptor()
        
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'dockovalent', 'yes')
        # after rounds 1-9
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'ang1_step', '3.5')
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'ang2_step', '3.5')
        #  after rounds 13-16
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'bump_maximum', '100.0')
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'bump_rigid', '100.0')        
        
        self.run_docking()
        self.post_dock()

    def Create_DB2_file(self):
        """creates DB2.gz file out of smiles representation of the ligand"""
        os.chdir(self.path)
        sp.call("$DOCKBASE/ligand/generate/build_smiles_ligand.sh xtal-lig.smi --covalent", shell=True)
        os.chdir(self.current_location)

    def Create_DB2_file_crys(self):
        """creates DB2.gz file out of smiles representation of the ligand"""
        run_dir = 'db2_files'
        os.chdir(self.path)
        sp.call('mkdir ' + run_dir, shell=True)
        os.chdir(run_dir)
        sp.call('cp ../tmp.pdb .', shell=True)
        sp.call('{0}/ligand/generate/crys_build_ligand.sh tmp.pdb'.format(Paths.DOCKBASE), shell=True)
        sp.call('mv tmp.db2.gz ../xtal-lig.db2.gz', shell=True)
        os.chdir(self.current_location)
        
    def Prepare_Receptor(self):
        """prepare receptor for docking"""
        os.chdir(self.path)
        sp.call("$DOCKBASE/proteins/blastermaster/blastermaster.py --covalentResNum {0} --covalentResName {1} --covalentResAtoms {2}".format(self.covalent_res.id[1], self.covalent_res.resname, self.covalent_atom_dict[self.covalent_res.resname]), shell=True) 
        os.chdir(self.current_location)    
        
    def _changeIndock(self):
        """
        Deprecated!!!
        
        changes the folowing parameters:
            1. bump_maximum 10.0 to 1000.0
            2. bump_rigid 10.0 to 1000.0
            3. dockovalent to yes
        """
        INDOCK = "/".join([self.path, "INDOCK"])
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

    def run_docking(self):
        """runs the docking itself after changing the right parameters  in indock file"""
        
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'dockovalent', 'yes')
        # after rounds 1-9
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'ang1_step', '3.5')
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'ang2_step', '3.5')
        #  after rounds 13-16
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'bump_maximum', '100.0')
        self.changesINDOCK("/".join([self.path, "INDOCK"]),'bump_rigid', '100.0')  
        
        os.chdir(self.path)
        folder_name = self.DOCKING_RUN 
        docking_job = DOCKovalent.DOCKovalent(self.DOCKING_RUN, "xtal-lig.db2.gz")
        os.chdir(self.current_location)
        
    def post_dock(self):
        path = self.path + "/" +  self.DOCKING_RUN
        
        #prepare for combine script
        open(path + "/dirlist", 'w').write("out")# create dirlist file 
        os.mkdir(path + "/out")
        sp.call('mv {0}/OUTDOCK {0}/test.mol2.gz {0}/out'.format(path), shell=True)
        
        #combine 
        os.chdir(path)
        sp.call([Paths.DOCKBASE + "analysis/extract_all.py", "--done"])
        sp.call([Paths.DOCKBASE + "analysis/getposes.py"])

        #rmsd - first removes all hydrogens 
        sp.call('python {0}/CovaLib/Scripts/rmsd.py -ref ../ligand_org.mol2 -in poses.mol2 -overlay false'.format(os.environ['HOME']), shell=True)
        self.rmsd = open('rmsd.txt','r').read()
        print 'rmsd: ', self.rmsd
        os.chdir(self.current_location)

    def changesINDOCK(self, path, parameter, value):
        indock = open(path, 'r').readlines()        
        new_indock = list()
        for line in indock:
            if parameter in line:
                new_indock.append('{0: <30}{1}\n'.format(parameter, str(value)))
            else:
                new_indock.append(line)
        open(path,'w').writelines(new_indock)



def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]
        rb = Benchmark(path)
        rb.run()                        

def print_usage(name):
        print "Usage : " + name + " <preparing_files_directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

