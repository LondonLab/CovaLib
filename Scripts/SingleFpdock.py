import sys
sys.path.append("/home/labs/londonir/danielza/CovaLib")
from Code import *
import subprocess
import os
import re
import numpy as np
import shutil
from subprocess import Popen

def main(name, argv):
    if (not len(argv) == 3):
        print_usage(name)
        return
    seq = argv[2]
    start = argv[0]
    cst = os.path.abspath(argv[1])
    write_res_file(seq, "resfile")
    PyUtils.create_softlink(start, './start.pdb')
    logfile = open("log.design", 'w')
    #Run the design
    subprocess.call([Paths.ROSETTA + "fixbb.linuxclangrelease", "-s", "start.pdb", "-resfile", "resfile", "-nstruct", "1"], stdout = logfile)
    logfile.close()
    #Run FlexPepDock
    PyUtils.create_folder("fpdock")
    os.chdir("fpdock")
    PyUtils.create_softlink("../start_0001.pdb", "./start.pdb")
    PyUtils.create_softlink(cst, "./cst")
    logfpdock = open("fpdock.log", 'w')
    decoys = "decoys.silent"
    subprocess.call([Paths.ROSETTA + "FlexPepDocking.linuxclangrelease", "-s", "start.pdb", "-native", "start.pdb", "-ex1", "-ex2aro", "-pep_refine", "-nstruct", "100", "-cst_fa_file", "cst", "-cst_fa_weight", "1.0", "-out:file:silent", decoys, "-out:file:silent_struct_type", "binary"], stdout = logfpdock)
    logfpdock.close()
    #Get best model in several categories
    score_file = open("../SCORES", 'w')
    for line in open(decoys):
        if re.search("SCORE", line):
            score_file.write(line)
    score_file.close()
    intColumn = np.array([float(i) for i in PyUtils.getNcolumn('../SCORES', 25)[1:]])
    pepColumn = np.array([float(i) for i in PyUtils.getNcolumn('../SCORES', 27)[1:]])
    int_score_ranked = np.argsort(intColumn)
    pep_score_ranked = np.argsort(pepColumn)
    int_best_sc = np.sort(intColumn)
    pep_best_sc = np.sort(pepColumn)
    int_best = "start_%04d" % (int_score_ranked[0] + 1)
    pep_best = "start_%04d" % (pep_score_ranked[0] + 1)
    best_scores = open("../Best_scores", 'w')
    best_scores.write("Int score:\n")
    best_scores.write(str(int_best_sc[0]) + '\n')
    best_scores.write("Pep score:\n")
    best_scores.write(str(pep_best_sc[0]) + '\n')
    best_scores.close()
    subprocess.call([Paths.ROSETTA + "extract_pdbs.linuxclangrelease", "-in::file::silent", decoys, "-in::file::tags", int_best, "-in::file::silent_struct_type", "binary", "-out::prefix", "int_score."])
    subprocess.call([Paths.ROSETTA + "extract_pdbs.linuxclangrelease", "-in::file::silent", decoys, "-in::file::tags", pep_best, "-in::file::silent_struct_type", "binary", "-out::prefix", "pep_score."])
    shutil.move("int_score." + int_best + ".pdb", "../int_best.pdb")
    shutil.move("pep_score." + pep_best + ".pdb", "../pep_best.pdb")
    os.remove(decoys)
    os.chdir("../")

def write_res_file(seq, file_name):
    f = open(file_name, 'w')
    f.write("NATRO\n")
    f.write("start\n")
    for i in range(len(seq)):
        f.write(str(i + 1) + " W PIKAA " + seq[i] + " EX 1 EX 2\n")

def print_usage(name):
    print "Usage : " + name + " <start_file> <constraints_file> <sequence>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
