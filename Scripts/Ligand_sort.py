import sys,os,math
import numpy as np
sys.path.append("/home/dinad/CovaLib")
from Code import *

def generate_score_for_lig(pose):
    sp = pose.split()
    score = int(sp[8]) + 0.5*int(sp[5])- 2*int(sp[7])
    if float(sp[4]) < -1 or float(sp[4])> 0: score -= 10
    scored = pose.strip() + ' ' + str(score) + '\n'
    return scored

def sort_list_by_scores(PDBid,score_col,score_name):
    unsorted = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_sort.txt','r').readlines()
    sorted_list = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_sorted.txt','a')
    data = []
    for line in unsorted:
        line = line.split()
        data.append(line)
    data.sort(key=lambda s:(float(s[score_col])),reverse=True)
    for line in data:
        line = ' '.join(line)+'\n'
        sorted_list.write(line)

def create_new_mol2(PDBid,score_name):
    path = os.getcwd()+'/'+score_name+'/'
    sorted_list = open(path+PDBid+'_ligand_sorted.txt','r').readlines()
    new_mol =  open(path+PDBid+'_sorted_poses.mol2','a')
    poses_f = Poses_parser.Poses_parser(os.getcwd()+'/'+PDBid+'/run.alk_hal.frag/poses.mol2')
    for line in sorted_list:
        line = line.split()
        lig = poses_f.get_lig(int(line[1])-1)
        for l in lig:
            new_mol.write(l)

        
    
def main(name, argv):
    if (len(argv) != 1):
        print_usage(name)
        return
    PDB_list = open(os.getcwd()+'/'+argv[0],'r').readlines()
    score_name = 'buried_with_all'
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        print PDBid
        Lig_score = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_score.txt','r').readlines()
        outfile_local = open(os.getcwd()+'/'+score_name+'/'+PDBid+'_ligand_sort.txt','a')
        for pose in Lig_score:
            outfile_local.write(generate_score_for_lig(pose))
        outfile_local.close()

        sort_list_by_scores(PDBid,9,score_name)
                
        create_new_mol2(PDBid,score_name)

def print_usage(name):
    print "Usage : " + name + " <PDB_list_file>"


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

