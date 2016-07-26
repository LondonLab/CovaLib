import subprocess as sp
import sys
from pprint import pprint
import Bio.PDB as bp
import os
#sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
#from Code import Paths


class Finder(object):
    def __init__(self, pdb_path, ligand_name, covalent_distance = 2):
        """
        pdb_path - location of pdb file containing the ligand and the receptor
        ligand_name - ligand's name in pdb file
        covalent_distance - the maximal distance between two covalent atoms
        """
        self.path = pdb_path 
        self.covalent_distance = covalent_distance
        self.receptor_name = self.path.split('/')[-1][: self.path.rfind('.')]
        self._read_pdb()
        self._find_ligand(ligand_name)
        self._find_covalent_atom()
    
    def _read_pdb(self):
        """reads the input pdb as a structre object from BioPython"""
        parser = bp.PDBParser()
        self.structure = parser.get_structure(self.receptor_name, self.path)
        
    def _find_ligand(self, ligand_name):
        ligands = [ res for res in self.structure.get_residues() if res.id[0] == 'H_'+ligand_name]
        if len(ligands) !=1:
            ve = ValueError()
            ve.message = ("More than one ligand having the name "  if len(ligands) > 1 else "Couldn't find ligand") + ligand_name
            raise ve
        self.ligand = ligands[0]
        
    def _find_covalent_atom(self):
        atoms = list(self.ligand.get_atom())#ligand atoms
        for res in self.structure.get_residues():
            if res.id[0] == ' ':#add all residues atoms
                atoms = atoms + res.get_list()
        ns = bp.NeighborSearch(atoms)
        neighbors = ns.search_all(self.covalent_distance)
        
        covalent = [cpl for cpl in neighbors if (cpl[0].parent.id[0] == ' ' and cpl[1].parent.id == self.ligand.id) or (cpl[0].parent.id == self.ligand.id and cpl[1].parent.id[0] == ' ' )] # filter only intermolecule bonds      
        covalent = [cpl for cpl in covalent if not (cpl[0].name.startswith('H') or cpl[1].name.startswith('H'))] #filter Hydrogens
        cov_cpl = min(covalent, key = lambda cpl: abs(cpl[0] - cpl[1]))
        
        ## decouple ligand & receptor covalent atoms
        self.receptor_cov_atom = [atom for atom in cov_cpl if atom.parent.id[0] == ' '][0]
        self.ligand_cov_atom = [atom for atom in cov_cpl if atom.parent.id == self.ligand.id][0]
        
    def get_receptor_covalent(self):
        """get a Bio PDB atom object of the covalent atom of the receptor"""
        return self.receptor_cov_atom
    
    def get_ligand_covalent(self):
        """get a Bio PDB atom object of the covalent atom of the ligand"""
        return self.ligand_cov_atom
        
    def print_result(self):
        print 'ligand   covalent atom:'
        print ' name:', self.ligand_cov_atom.name, 'chain:', self.ligand_cov_atom.parent.parent.id, 'resseq:', self.ligand_cov_atom.parent.id[1]
        print 'receptor covalent atom:'
        print ' name:', self.receptor_cov_atom.name, 'chain:', self.receptor_cov_atom.parent.parent.id, 'resseq:', self.receptor_cov_atom.parent.id[1]

    
def main(name, argv):
    if(len(argv) != 2):
        print_usage(name)
        return
    f= Finder(argv[0], argv[1])
    f.print_result()
    pass
            
def print_usage(name):
        print "Usage : " + name + " <pdb_path>  <ligand_name>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
