import sys,os,math
from os import path
from os import listdir
from os.path import isfile, join
import Bio.PDB
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
import subprocess

def main(name, argv):
    if (len(argv) <> 3):
            print_usage(name)
            return
    start_res = int(argv[1])
    end_res   = int(argv[2])
    mypath = argv[0]
    abspath = os.getcwd()
    onlyfiles = [abspath+"/"+mypath + a for a in listdir(mypath) if isfile(join(mypath, a))]
    for fi in onlyfiles:
        Check_for_loop(mypath, fi, start_res, end_res)
        Check_for_AB(mypath,fi)
    return()

def Check_for_loop(path, file_checked, start_id, end_id):
    pdb_parser = Bio.PDB.PDBParser(QUIET = True)
    structure = pdb_parser.get_structure("file_checked", file_checked)
    model = structure[0]
    list_res_id = []
    ref_res_id = range(start_id, end_id+1)
    for chain in model:
            for res in chain:
                    if res.get_id()[1] in ref_res_id:
                            list_res_id.append(int(res.get_id()[1]))
                            
    ouf = open('list_odd_files.txt', 'a')
    if len(list_res_id) <> len(ref_res_id):
            ouf.write(file_checked[-9:])
            ouf.write(' ')
    ouf.close()


def Check_for_AB(path, file_checked):
    subprocess.call(["/work/londonlab/scripts/pdbUtil/extract_chains_and_range.pl", "-p", file_checked, "-c", file_checked.split("/")[-1][4:5], "-o",file_checked])
    return()
    
def print_usage(name):
    print "Usage : " + name + "<Folder> <start_id_loop> <end_id_loop>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
