import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def analize(PDBid,score_name):
    sorted_f = open('./'+score_name+'/'+PDBid+'_ligand_sorted.txt','r').readlines()
    total = len(sorted_f)
    filtered_out = 1500 - total
    resqued = 0
    mean_score = 0
    max_range = 0
    mean_top_10 = 0
    if total > 500: max_range = 500
    else: max_range = total
    for i in range(max_range):
        sp_line = sorted_f[i].split()
        orig_score = int(sp_line[2])
        if orig_score > 500:
            resqued += 1
        mean_score += float(sp_line[len(sp_line)-1])
        if i < 10:
            mean_top_10 += float(sp_line[len(sp_line)-1])
    mean_score ='%.2f' % (mean_score/max_range)
    mean_top_10 = '%.2f' % (mean_top_10/10)
    return filtered_out, resqued, mean_score, mean_top_10

def main(name, argv):
    if (len(argv) != 1):
        print_usage(name)
        return
    
    score_name = '13_04_alpha-sub-acrylate-esters.frag'
    outfile = open('./'+score_name+'/'+'analize.txt','a')
    PDB_list = open(os.getcwd()+'/'+argv[0],'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        print PDBid
        ana = analize(PDBid,score_name)
        outfile.write(PDBid +' '+' '.join(str(x) for x in ana)+'\n')

def print_usage(name):
    print "Usage : " + name + PDBid_list


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

