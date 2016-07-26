import subprocess as sp
import sys
from pprint import pprint
import Bio.PDB as bp
import re
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import Paths, SMIUtil
import math

OUTPUT_DIRECTORY = "Preparation"
DIHEDRAL_OUTPUT = 'dihedral'

class Prepare(object):
    def __init__(self, name, path, summary):
        """
        Creates all files needed for Preparering ligand & receptor for docking.
        
        initializes:
            covalent_dummy_atom_dict - dictionary that specifies for every AA its covalent atom's name 
            receptor_name
            path - path to drectory where all the files should be
            covalent_res_dict - see function _parse_summary_line
            ligand_dict - see function _parse_summary_line
            file - see function _read_file
            structre - see function _read_file 
            ligand - see function _find_ligand
            covalent_res - see function _find_covalent_res
            covalent_atm_res - see function _find_covalent_res
        
        creating files:
            1. pdb of the receptor
            2. summary_line - contains the summary line for creating this directory
        """
        print 'in init'
        self.covalent_atom_dict = {'CYS':'HG', 'THR':'HG1'}
        self.covalent_dummy_atom_dict = {'CYS':'SG'} #########check
        
        #set input
        self.receptor_name = name
        self.path = path
        self._parse_summary_line(summary)
        
        #set files
        self.current_location = os.getcwd()
        self._download_pdb()
        self._read_file()
        
        #set ligand and covalent residue
        self._find_ligand()
        self._find_covalent_res()
    
    def _parse_summary_line(self, summary):
        """
        parsing the summary line of the current receptor.
        summary line format:
        e.g. : 1aec    A         25     219    E64     N-[N-[1-HYDROXYCARBOXYETHYL-CARBONYL]LEUCYLAMINO-BUTYL]-GUANIDINE        C2     A        219    1.80
        receptor-pdbID  receptor's-covalent-atom-chain   receptor's-covalent-atom-resswq    ligand's-covalent-atom-resseq   ligand's-name   
        ligand-formula  ligand's-covalent-atom-name ligand's-covalent-atom-chain    ligand's-covalent-atom-resseq   some-value0(I think bond length)
        
        initializes:
            covalent_res_dict - dictionary containing the chain & resseq of the receptor's covalent residue
            ligand_dict - dictionary containing the chain, resseq & covalent atom's name of the ligand
        """
        
        # saving the summary line in a txt file
        open(self.path + '/summary_line','w').write(summary)
        
        #parsing 
        summary_list = summary.split()
        self.covalent_res_dict = {'chain':summary_list[1], 'resseq':int(summary_list[2])}
        self.ligand_dict = {'name':summary_list[4], 'chain':summary_list[-3], 'resseq':int(summary_list[3]), 'cov_atm': summary_list[-4]}
           
    def _download_pdb(self):
        """
        downloading the receptor's pdb
        """
        os.chdir(self.path)
        sp.call(["wget", "http://www.rcsb.org/pdb/files/" + self.receptor_name + ".pdb"])
        os.chdir(self.current_location)

    def _read_file(self):
        """
        reads the input pdb as a list and as a structre object from BioPython.
        initializes:
            self.file - file as a list
            self.structure - receptor's pdb as a Bio PDB structure object
        """
        pdb_path = '{0}/{1}.pdb'.format(self.path, self.receptor_name)
        
        #read as list
        self.file = open(pdb_path, 'r').readlines()
        
        #read as Bio PDB object
        parser = bp.PDBParser()
        self.structure = parser.get_structure(self.receptor_name, pdb_path)

    def _find_ligand(self):
        """
        Saves the ligand as a residue Bio PDB object.
        initializes:
            ligand
        """
        self.ligand = self.structure[0][self.ligand_dict['chain']][("H_"+self.ligand_dict['name'], self.ligand_dict['resseq']," ")]
        
    def _find_covalent_res(self):
        """
        Saves the covalent residue & atom of the receptors as residue $ atom bio PDB objects.
        covalent_res - receptor's covalent residue
        covalent_atm_res - receptor's covalent atom 
        """
        self.covalent_res = self.structure[0][self.covalent_res_dict['chain']][self.covalent_res_dict['resseq']]
        self.covalent_atm_res = self.covalent_res.child_dict[self.covalent_dummy_atom_dict[self.covalent_res.resname]]
   
    def run(self):
        """Creates files to run the benchmark"""
        self.create_ligand_files()
        self.correct_receptor_pdb()          
        
    def create_ligand_files(self):
        """
        Creats different versions of the ligand for later steps in the Docking procedure
        Creates files:
            xtal-lig.pdb - the ligand in a PDB format
            ligand_org.mol2 - the ligand in mol2 format
            xtal-lig.smi - the ligand + Si dummy atom in smiles format
            tmp.pdb - ligand's pdb + the dummy atom
            
        """
        
        # finds all ligand lines in the receptor's PDB file
        pattern = "HETATM.*{0}.*{1}.*{2}.*".format(self.ligand.resname, self.ligand.parent.id, self.ligand.id[1])
        lig_lines = [line for line in  self.file if re.search(pattern,line) !=  None]
        
        if lig_lines[-1][16] != ' ': # has Alternate location indicator
            lig_lines = [line for line in lig_lines if line[16] == 'A']
        
        #create pdb from ligand for preparing the receptor later
        ligand_pdb = self.path +'/xtal-lig.pdb'
        open(ligand_pdb, 'w').writelines(lig_lines)
        
        #create mol2 file out of original ligand (to compare rmsd value after docking)
        sp.call('convert.py {0} {1}/ligand_org.mol2'.format(ligand_pdb, self.path), shell=True)

        #create line of dummy atom to add to the ligand's pdb
        dummy_atm = self._get_atm_str(self.covalent_atm_res)
        tmp = self._parse_hetatm_line(lig_lines[-1]) #the last atom of the original ligand, to get indexes for the dummy atom
        lig_lines.append("HETATM{0: >5}{1: >5}{2:>4}{3:>2}{4:>4}{5:>40}{6:>12}\n".format
                         (int(tmp[1])+1, 
                          "Si1", 
                          tmp[3], 
                          tmp[4], 
                          tmp[5], 
                          dummy_atm[26:66], 
                          "Si"))
        
        #save as smiles format + (protonated) Si
        file_name = self.path+"/"+"tmp.pdb"
        open(file_name,'w').writelines(lig_lines)
        smiles_file_name = self.path + '/xtal-lig.smi'
        sp.call("convert.py {0} {1}".format(file_name, smiles_file_name), shell=True)
        #os.remove(file_name)
        smiles = open(smiles_file_name, 'r').read()
        smiles = smiles.replace("Si","SiH3")
        smiles = SMIUtil.get_canonical_smiles(smiles.strip()) #removes stereo isomers information
        smiles = smiles.strip() + " xtal-lig\n" #for converting to db2
        open(smiles_file_name, 'w').write(smiles)
            
    def _get_atm_str(self,atm):
        """
        Given an atom (of the receptor's residues) object, returns it's line in the receptor's PDB file
        """
        pattern = "ATOM.*{0}.*{1}.*".format(atm.id, atm.parent.id[1])
        return [line for line in self.file if re.search(pattern,line)!= None][0]
        
    def _parse_hetatm_line(self, line):
        """
        Parses a HETATM PDB line and returns it as a list
        """
        components = []
        # 0- HETATM
        components.append(line[0:6].strip())
        # 1-atom serial number
        components.append(line[6:11].strip())
        # 2-atom name
        components.append(line[12:16].strip()) 
        # 3-residue\ligand name
        components.append(line[17:20].strip())
        # 4- chain
        components.append(line[21].strip())
        # 5- resseq\ Residue sequence number           
        components.append(line[22:26].strip())
        # 6- all the rest :)
        components.append(line[26:].strip())     
        # 7- Alternate location indicator
        components.append(line[16])  
        return components
    
    def correct_receptor_pdb(self): 
        """
        Cleans receptor file from original ligand
        Creates files:
            rec.pdb - only the receptor's chain having the covalent residue
        """
        rec_file = self.path+"/rec.pdb"
        sp.call("/work/londonlab/scripts/pdbUtil/extract_chains_and_range.pl -p {0} -c {2} -o {1}".format
                ('{0}/{1}.pdb'.format(self.path, self.receptor_name), # path to original receptor
                 rec_file,                                            # path to new, clean receptor
                 self.covalent_res_dict['chain']),shell=True)         # chain of receptor to extract
        
        # concatinating to the end of the clean receptor file information form the summary line
        l = open(rec_file,'r').readlines()
        l.append("REMARK @@@ covalent residue id {0}\n".format(self.covalent_res.id[1]))
        l.append("REMARK @@@ covalent residue name {0}\n".format(self.covalent_res.resname))
        l.append("REMARK @@@ covalent residue chain {0}\n".format(self.covalent_res_dict['chain']))
        l.append("REMARK @@@ covalent residue lig_name {0}\n".format(self.ligand.resname))
        l.append("REMARK @@@ covalent residue lig_chain {0}\n".format(self.ligand.parent.id))
        open(rec_file,'w').writelines(l)
    
    def print_covalent_res(self):
        """
        Debug Printing
        """
        print "Chain:  ", self.covalent_res_dict['chain']
        print "Name:   ", self.covalent_res.resname
        print "ID:     ", self.covalent_res.id[1]
        print "Ligand: ", self.ligand.resname
        print "ligand chain", self.ligand.parent.id
         
    def analyze_dihedral(self):  
        """
        Deprecated. Please use class Dihedral_Analisys
        """
        angles = list()
        cov_atm_lig = self.ligand.child_dict[self.ligand_dict['cov_atm']]
        ##dihedral between CA < CB < SG < ligand
        angle_1 = math.degrees( bp.calc_dihedral(self.covalent_res.child_dict['CA'].get_vector(),
                                                 self.covalent_res.child_dict['CB'].get_vector(),
                                                 self.covalent_atm_res.get_vector(),
                                                 cov_atm_lig.get_vector()))
        angles.append(angle_1)
        ##all dihedral of CB < SG < ligand-covalent-atom < other ligand atoms
        ns  = bp.NeighborSearch(list(self.ligand.get_atom()))        
        neigh = ns.search(cov_atm_lig.get_coord(), 2) 
        neigh = filter(lambda x: x.name != self.ligand_dict['cov_atm'], neigh)# removes the atom itself
        for i in neigh:
            ang = math.degrees( bp.calc_dihedral(self.covalent_res.child_dict['CB'].get_vector(),
                                                 self.covalent_atm_res.get_vector(),
                                                 cov_atm_lig.get_vector(),
                                                 i.get_vector()))
            angles.append(ang)
        open('/'.join([self.path, DIHEDRAL_OUTPUT]), 'w').write(reduce(lambda x, ang: ' '.join([x, str(ang)]), angles, ''))
        
def main(name, argv):
    if(len(argv) != 2):
        print_usage(name)
        return
    prep = Prepare(argv[0], os.getcwd(), '  '.join(argv[1:])) 
    prep.run()
            

def print_usage(name):
        print "Usage : " + name + " <pdb_id>  <summary_line>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
