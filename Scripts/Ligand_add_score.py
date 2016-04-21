#from __future__ import print_function
import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
from openeye.oechem import *

def dist (a1,a2):
    a1 = [float(x) for x in a1]
    a2 = [float(x) for x in a2] 
    return math.sqrt((a1[0]-a2[0])*(a1[0]-a2[0])+(a1[1]-a2[1])*(a1[1]-a2[1])+(a1[2]-a2[2])*(a1[2]-a2[2]))

def check_for_reactive_gr(smiles):
    mol = OEGraphMol()
    OESmilesToMol(mol, smiles)
    matches = 0
    for pat in ['[C;H2][Cl,Br,I]']:
        ss = OESubSearch(pat)
        OEPrepareSearch(mol, ss)
        for count, match in enumerate(ss.Match(mol)):
            matches += count+1
    if matches == 0: return 'good'
    else: return 'rg2'

def count_bonds(lig,rec,rec_oths):#,LEN_HYD_BOND):
    LEN_HYD_BOND = 2.5
    num_hyd_bonds = 0
    num_unsut = 0
    num_unsut_buried = 0
    num_bonded_lig_atms = 0
    num_bonded_rec_atms = 0
    for lig_atom in lig:
        bond_per_atom = 0
        for rec_atom in rec:
            bond_len = dist(lig_atom,rec_atom)
            if bond_len<LEN_HYD_BOND:
#                print [lig_atom,rec_atom,bond_len]
                num_hyd_bonds +=1
                bond_per_atom +=1
        if bond_per_atom == 0:
            num_unsut +=1
            num_neighbors = 0
            for oth in rec_oths:
                bond_len = dist(lig_atom,oth)
                if bond_len < LEN_HYD_BOND+2:
                     num_neighbors +=1
            if num_neighbors > 1:
                num_unsut_buried +=1
        else: num_bonded_lig_atms += 1
    return num_hyd_bonds, num_unsut, num_unsut_buried, num_bonded_lig_atms

def main(name, argv):
    if (len(argv) != 1):
        print_usage(name)
        return
    path = os.getcwd()
    PDB_list = open(path+'/'+argv[0],'r').readlines()  
    outfile = open(path+'/ligand_score.txt','a')
    score_name = 'for-sale'
    addition_name = '_rg2'
    PyUtils.create_folder(score_name)
    score_path = path+'/'+score_name+'/'
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        print PDBid
        rec_path = path+'/'+PDBid+'/working/rec.crg.pdb'
        rec_f = Poses_parser.rec(rec_path)
        rec_dons, rec_accs, rec_oths, rec_all = rec_f.get_rec_don_acc()
        old_outfile = open(score_path+'/'+PDBid+'_ligand_score.txt','r').readlines()
        new_outfile = open(score_path+'/'+PDBid+addition_name+'_ligand_score.txt','a')
        mol_path = path+'/'+PDBid+'/run.alk_hal.lead-1/poses.mol2'
        poses_f = Poses_parser.Poses_parser(mol_path)
        len_poses = poses_f.get_len_poses()
        print poses_f.get_len_poses()
        for x in range(len_poses-1):
            print PDBid+' '+str(x)
            smiles = poses_f.get_smiles(x)
            rg = check_for_reactive_gr(smiles)
            new_outfile.write(old_outfile[x].strip()+' '+rg+'\n')
            
def print_usage(name):
    print "Usage : " + name + " <PDB_list_file>"


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

