import os
import PyUtils
import subprocess
def DownloadPDBs(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        PyUtils.create_folder(os.getcwd()+"/"+PDBid)
        os.chdir(PDBid)
        cmd = ["~/../scripts/pdbUtil/getPdb.pl"+" -id "+PDBid]
        subprocess.call(cmd,shell=True)
        os.chdir("..")

def rec(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        os.chdir(PDBid)
        subprocess.call(["~/../scripts/pdbUtil/extract_chains_and_range.pl -p "+PDBid.lower()+".pdb -c "+PDB_list[i].split()[1]+" -o rec.pdb"],shell=True)
        os.chdir("..")

def lig(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        sp_PDB = PDB_list[i].split()
        PDBid = sp_PDB[0]  
        os.chdir(PDBid)
        PDBf_name = PDBid.lower()+".pdb"
        PDBf = open(PDBf_name).readlines()
        lig_f = open(os.getcwd()+'/xtal-lig.pdb','w')
        for line in PDBf:
            if line.startswith('HETATM'):
                sp_line = line.split()
                if len(sp_line) == 12:
                    if sp_line[3] == sp_PDB[2] and sp_line[4] == sp_PDB[1] and sp_line[5] == sp_PDB[3]:
                        lig_f.write(line)
                if len(sp_line) == 11:
                    if sp_line[3] == sp_PDB[2] and sp_line[4][0:1] == sp_PDB[1] and sp_line[4][2:] == sp_PDB[3]:
                        lig_f.write(line)
        lig_f.flush()
        os.chdir("..")

'''
#reading rec.crg.pdb file lines
class rec_atom:
    def __init__(self, num, atom, res, chain, res_num, x, y, z, pre, b_fac, 1atom):
        self.num = num
        self.atom = atom
        self.res = amino
        self.chain = chain
        self.res_num = res_num
        self.x = x
        self.y = y
        self.z = z
        self.pre = pre
        self.b_fac = b_fac
        self.1atom = 1atom
    @staticmethod
    def read_rec_line(raw_line):
        line = re.findall(r'[-+]?\d*\.\d+|\d+$',raw_line)
        return Point(float(line[0]),float(line[1]),float(line[2]))       
                                                                                                                                                                                                     
                sp_line = line.split()                                                                                                                                                                  
                if line[1] in possible_ligs:                                                                                                                                                            
                    continue                                                                                                                                                                            
                else:                                                                                                                                                                                   
                    possible_ligs.append(line[1])                                                                                                                                                       
            else: continue                                                                                                                                                                              
        if len(possible_ligs)>1:                                                                                                                                                                        
            ligand = input("choose ligand for "+PDBid+" from: "+ str(possible_ligs))                                                                                                                    
        else: ligand = possible_ligs[0]'''
