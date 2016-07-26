#Written by Daniel Zaidman                                                                                                                                                                                                                                                    
#Code review by                                                                                                                                                                                                                                                               

import sys,os,math
sys.path.append(os.environ["COVALIB"])
from Code import *
import subprocess
import shutil

def main(name, argv):
        if not len(argv) == 5:
                print_usage(name)
                return

	clu = Cluster.Cluster()
	with open('LOOP_FILE' , 'w') as f_write:
		f_write.write('LOOP ' + argv[1] + ' ' +  argv[2] + ' 0 0 1\n')
	clu.runCommandsArgs('/work/londonlab/Rosetta/main/source/bin/loopmodel.default.linuxgccrelease -s ' + argv[0] + ' -native ' + argv[0] + ' @' + argv[3] + ' -overwrite true -out:prefix', range(int(argv[4])))

def print_usage(name):
        print "Usage : " + name + " <loop_pdb_file> <start_res> <end_res> <flags_file> <num_of_runs>"

if __name__ == "__main__":
        main(sys.argv[0], sys.argv[1:])
