import sys,os,math
import numpy as np
sys.path.append("/home/labs/londonir/dinad/CovaLib")
from Code import *

def dist (a1,a2):
    a1 = [float(x) for x in a1]
    a2 = [float(x) for x in a2] 
    return math.sqrt((a1[0]-a2[0])*(a1[0]-a2[0])+(a1[1]-a2[1])*(a1[1]-a2[1])+(a1[2]-a2[2])*(a1[2]-a2[2]))

def count_bonds(lig,rec,rec_oths):#,LEN_HYD_BOND):
    LEN_HYD_BOND = 2.5
    num_hyd_bonds = 0
    num_unsut = 0
    num_unsut_buried = 0
    num_bonded_lig_atms = 0
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
   
    path = argv[0]
    rec_path = '/home/labs/londonir/dinad/Pin1/docking/4tns/working/rec.crg.pdb.polarH'
    rec_f = Poses_parser.rec(rec_path)
    rec_dons, rec_accs, rec_oths = rec_f.get_rec_don_acc()
    poses_f = Poses_parser.Poses_parser(path)
    for x in range(0,499):
        lig_dons,lig_accs = poses_f.find_lig_don_acc(x)
        tot_hyd_bonds = 0
        tot_unsut = 0
        tot_unsut_buried = 0
        num_bonded_lig_atms = 0
        cb = count_bonds(lig_dons,rec_accs,rec_oths)
        tot_hyd_bonds += cb[0]
        tot_unsut += cb[1]
        tot_unsut_buried += cb[2]
        num_bonded_lig_atms +=cb[3]
        cb = count_bonds(lig_accs,rec_dons,rec_oths)
        tot_hyd_bonds += cb[0]
        tot_unsut += cb[1]
        tot_unsut_buried += cb[2]
        num_bonded_lig_atms +=cb[3]
        print [ligand,x+1,tot_hyd_bonds,tot_unsut,tot_unsut_buried,num_bonded_lig_atms]

def print_usage(name):
    print "Usage : " + name + " <PDB_list_file>"


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
