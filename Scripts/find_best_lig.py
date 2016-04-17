import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
    if (len(argv) != 0):
        print_usage(name)
        return
    score_name = '12-04_03_lead'
    outfile = open('./'+score_name+'/chosen_sum1.txt','a')
    ls = os.listdir('./'+score_name)
    chosen_PDBs = []
    for f in ls:
        if f.endswith('sorted_poses.mol2'): chosen_PDBs.append(f)
    ligs = []
    for mol in chosen_PDBs:
        mol_path = './'+score_name+'/'+mol
        poses_f = Poses_parser.Poses_parser(mol_path)
        len_poses = poses_f.get_len_poses()
        for x in range(len_poses-1):
            lig_name,size,charge = poses_f.get_lig_properties(x)
            ligs.append(lig_name)
    output = []
    prev_ligs = []
    for lig in ligs:
        cnt_lig = ligs.count(lig)
        if lig not in prev_ligs:
            output.append(lig+' '+str(cnt_lig))
        prev_ligs.append(lig)
    outfile.write('\n'.join(output))
            
    

def print_usage(name):
    print "Usage : " + name + '<PDBid_list>'


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

