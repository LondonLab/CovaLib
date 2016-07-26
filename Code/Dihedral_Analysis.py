import sys
import os
from pprint import pprint
import subprocess as sp
import Bio.PDB as bp
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
import find_covalent_atom
import math


class Ligand_Dihedral(object):
    """
    this module calculates dihedral angles of a covalent bond:
        CA-CB-SG-LIG0
        CB-SG-LIG0-LIG1
        CB-SG-LIG0-LIG2
        CB-SG-LIG0-LIG3
    """
    def __init__(self,receptor_path, ligand_path):  
        self.receptor_path = receptor_path
        self.receptor = self.load_pdb(self.receptor_path, 'receptor')
        self.ligand_path = ligand_path
        self.load_ligand()
        self.set_covalent_atoms()
        self.calc_dihedral()        
        
    def load_pdb(self, path, name = 'unknown molecule'):
        return bp.PDBParser().get_structure(name, path)
    
    def load_ligand(self):
        if  self.ligand_path[-3:] == 'pdb':
            self.ligand = self.load_pdb(self.ligand_path, 'ligand')
            sp.call('cat {} {}>tmp_rec_lig.pdb'.format(self.receptor_path, self.ligand_path), shell=True)
            pdb_lig = self.ligand_path
        else:
        #if it's a mol2- I live in a world with only 2 file formats
            pdb_lig = 'tmp_ligand.pdb'
            sp.call('convert.py {0} {1}'.format(self.ligand_path, pdb_lig), shell=True)
            self.ligand = self.load_pdb(pdb_lig, 'ligand')
            os.remove(pdb_lig)
            
        self.rec_lig_pdb_path = 'tmp_rec_lig.pdb'
        sp.call('cat {} {}>{}'.format(self.receptor_path, pdb_lig, self.rec_lig_pdb_path), shell=True)
        
        
    def set_covalent_atoms(self):
        lig_name = [i for i in self.ligand.get_residues()][0].resname
        f = find_covalent_atom.Finder(self.rec_lig_pdb_path, lig_name)
        self.cov_receptor = f.get_receptor_covalent()
        self.cov_ligand = f.get_ligand_covalent()

    def calc_dihedral(self):
        cb = self.cov_receptor.parent['CB']
        ca = self.cov_receptor.parent['CA']
        lig_cov_neoghbors = self.get_atom_neighbors(self.cov_ligand, list(self.ligand.get_atoms()))
        self.angles = list()
        ang1 = math.degrees( bp.calc_dihedral(ca.get_vector(), 
                                              cb.get_vector(), 
                                              self.cov_receptor.get_vector(),
                                              self.cov_ligand.get_vector()))
        self.angles.append(ang1)
        for i in lig_cov_neoghbors:
            ang = math.degrees( bp.calc_dihedral(cb.get_vector(),
                                                 self.cov_receptor.get_vector(),
                                                 self.cov_ligand.get_vector(),
                                                 i.get_vector()))
            self.angles.append(ang)
            
    def get_dihedrals(self):
        return self.angles()
    
    def print_dihedral(self):
        print reduce(lambda x, ang: ' '.join([x, str(ang)]), self.angles, '')
        
        
    def get_atom_neighbors(self, atom, atoms, cov_dist = 2):
        ns = bp.NeighborSearch(atoms)
        neighbors = ns.search(atom.get_coord(), cov_dist)
        covalent = [atm for atm in neighbors if not (atm.name.startswith('H') or atm.name == atom.name)] #filter Hydrogens & the atom itself
        return covalent
               
def main(name, argv):
    if(len(argv) != 2):
        print_usage(name)
        return
    ld = Ligand_Dihedral(argv[0], argv[1])
    ld.print_dihedral()
        

def print_usage(name):
        print "Usage : " + name + " <receptor_path> <ligand_path>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

