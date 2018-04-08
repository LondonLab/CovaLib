import rdkit.Chem as rdk
import rdkit.Chem.AllChem as chm

def align(file_name1,file_name2,file_out): 
    mol1 = rdk.MolFromMol2File(file_name1)
    rdk.RemoveHs(mol1)
    mol2 = rdk.MolFromMol2File(file_name2)
    rdk.RemoveHs(mol2)
    rmds = chm.AlignMol(mol1,mol2)
    
    w = rdk.PDBWriter(file_out)
    w.write(mol1)
    w.close()
    
    return rmsd

def rmsdFirstConf(file_name_in,file_name_ref):
    in_mol = rdk.MolFromPDBFile(file_name_in)
    ref = rdk.MolFromPDBFile(file_name_ref)
    rmsd = chm.GetBestRMS(in_mol,ref,0,0)
    return file_name_in,rmsd

def rmsdAllConf(file_name_in,file_name_ref):
    rmsd_arr = []
    in_mol = rdk.MolFromPDBFile(file_name_in)
    ref = rdk.MolFromPDBFile(file_name_ref)
    for i,conf in enumerate(in_mol.GetConformers()):
        rmsd_arr.append(chm.GetBestRMS(in_mol,ref,i,0))
    return rmsd_arr


import sys
def main():
    file = sys.argv[1]
    ref = sys.argv[2]
    #print rmsdAllConf(file,ref)
    print rmsdFirstConf(file,ref)
  


if __name__ == "__main__":
    main()

