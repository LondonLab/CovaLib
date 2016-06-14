import sys
import os
from pprint import pprint
import subprocess as sp
import Bio.PDB as bp

from rdkit import Chem
from rdkit.Chem import Descriptors

class Filter_Bechmark(object):
    def __init__(self, path):  
        """
        path - location of the file where all results of running benchmark are
        """
        self.path = path 
        self.current_location = os.getcwd()
        
    def filter_by_ligand_size(self, less = 15, more = 40):   
        count_dict = dict()
        for subdir in os.listdir(self.path):
            if subdir.startswith('.'):
                continue
            pdb_path = self.path + subdir + '/xtal-lig.pdb'
            name = subdir.split('_')[0]
            count_dict[subdir] = self.count_heavy_atom(pdb_path, name)
        open('all','w').writelines(['{}    {}\n'.format(k, str(count_dict[k])) for k in count_dict ])
        #open('less_' + less,'w').writelines(['{}    {}\n'.format(k, str(count_dict[k])) for k in count_dict if count_dict[k] < less])
        #open('more_' + more,'w').writelines(['{}    {}\n'.format(k, str(count_dict[k])) for k in count_dict if count_dict[k] > more])
        #open('size','w').writelines(['{}    {}\n'.format(k, str(count_dict[k])) for k in count_dict if count_dict[k] >= less and count_dict[k] <= more])
              
    def count_heavy_atom(self, pdb_path, name = "rec"):
        """reads the input pdb as a list and as a structre object from BioPython"""
        parser = bp.PDBParser()
        structure = parser.get_structure(name, pdb_path)
        return len( [atm for atm in structure.get_atoms() if atm.element is not 'H']) 
    
    def filter_by_rotatable_bonds(self):
        for subdir in os.listdir(self.path):
            if subdir.startswith('.'):
                continue
            sp.call('convert.py {0}/{1}/ligand_org.mol2 {0}/{1}/tmp.smi'.format(self.path, subdir), shell=True)
            smiles = open('{0}/{1}/tmp.smi'.format(self.path, subdir),'r').read()
            os.remove('{0}/{1}/tmp.smi'.format(self.path, subdir))
            nRot = Descriptors.NumRotatableBonds(Chem.MolFromSmiles(smiles))    
            print subdir, nRot
 
               
def main(name, argv):
        if(len(argv) != 1):
            print_usage(name)
            return
        path = argv[0]
        fb = Filter_Bechmark(path)
        fb.filter_by_rotatable_bonds()


def print_usage(name):
        print "Usage : " + name + " <Run_directory>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

