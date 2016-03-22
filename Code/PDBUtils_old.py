import os
import PyUtils
import subprocess
def DownloadPDBs(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].strip()
        PyUtils.create_folder(os.getcwd()+"/"+PDBid)
        os.chdir(PDBid)
        cmd = ["~/../scripts/pdbUtil/getPdb.pl"+" -id "+PDBid]
        subprocess.call(cmd,shell=True)
        os.chdir("..")

def rec():
    folder_list = next(os.walk('.'))[1]
    for PDBid in folder_list:
        os.chdir(PDBid)
        subprocess.call(["~/../scripts/pdbUtil/extract_chains_and_range.pl -p "+PDBid.lower()+".pdb -c A -o rec.pdb"],shell=True)
        os.chdir("..")

def lig():
    folder_list = next(os.walk('.'))[1]
    for PDBid in folder_list:
        print PDBid
        os.chdir(PDBid)
        PDBf_name = PDBid.lower()+".pdb"
        PDBf = open(PDBf_name).readlines()
        possible_ligs = []
        for line in PDBf:
            if line.startswith('HET '):
                possible_ligs.append(line)
        [lig,chain,lig_num]=raw_input("choose ligand, a chain and ligand number for "+PDBid+" from:\n"+ str(possible_ligs)+'\n')
        print lig
        print lig_num
        lig_f = open(os.getcwd()+'/xtal-lig.pdb','w')
        for line in PDBf:
            if line.startswith('HETATM'):
                sp_line = line.split()
                if len(sp_line) == 12:
                    if sp_line[3] == lig and sp_line[4] == chain and sp_line[5] == lig_num:
                        lig_f.write(line)
                if len(sp_line) == 11:
                    if sp_line[3] == lig and sp_line[4][0:2] == chain and sp_line[4][2:] == lig_num:
                        lig_f.write(line)
                
        lig_f.flush()
        os.chdir("..")




                
'''                                                                                                                                                                                                     
                sp_line = line.split()                                                                                                                                                                  
                if line[1] in possible_ligs:                                                                                                                                                            
                    continue                                                                                                                                                                            
                else:                                                                                                                                                                                   
                    possible_ligs.append(line[1])                                                                                                                                                       
            else: continue                                                                                                                                                                              
        if len(possible_ligs)>1:                                                                                                                                                                        
            ligand = input("choose ligand for "+PDBid+" from: "+ str(possible_ligs))                                                                                                                    
        else: ligand = possible_ligs[0]'''
