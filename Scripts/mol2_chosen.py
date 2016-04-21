import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def get_pose(PDBid, Pose_num):
    outfile = open('./'+PDBid+'chosen.mol2','a')
    poses_f = Poses_parser.Poses_parser('./'+PDBid+'_sorted_poses.mol2')
    lig = poses_f.get_lig(int(Pose_num)-1)
    for l in lig:
        outfile.write(l)

def get_score(PDBid, Pose_num):
    outfile = open('./chosen.txt','a')
    infile = open('./'+PDBid+'_ligand_sorted.txt').readlines()
    line = infile[int(Pose_num)-1]
    outfile.write(line)

def main(name, argv):
    if (len(argv) != 2):
        print_usage(name)
        return
    PDBid = argv[0]
    Pose_num = argv[1]
    get_pose(PDBid,Pose_num)
    get_score(PDBid,Pose_num)

def print_usage(name):
    print "Usage : " + name + '<PDBid_list> + <pose_num>'


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

