import sys,os
sys.path.append("/home/labs/londonir/dinad/CovaLib")
from Code import *

def main(name, argv):
        if (len(argv) != 1):
                print_usage(name)
                return

#        arglist = []
#        dirfile = open(argv[0], 'r')
#        for line in dirfile:
#                arglist.append(line + " " + argv[1] + " " + argv[2])
        clu = Cluster.Cluster("CHEM")
        clu.runJobs(argv[0], "python $SCRIPTS/DOCKovalentTask.py run.alk_hal.frag /home/labs/londonir/Libraries/alkylhalides/frag True")

def print_usage(name):
        print "Usage : " + name + " <PDB_list_file>"# <compound/library path> <Library(True/False)>"


if __name__ == "__main__":
        main(sys.argv[0], sys.argv[1:])
