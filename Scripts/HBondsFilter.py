#Written by Daniel Zaidman                                                                                                                                                                                                                                                    
#Code review by                                                                                                                                                                                                                                                               

import sys,os,math
sys.path.append(os.environ["COVALIB"])
from Code import *
import subprocess
import shutil

def main(name, argv):
        if len(argv) < 2:
                print_usage(name)
                return
	
	hb_list = PosesHBonds.PosesHBonds(argv[0], argv[1:]).getList()
	l_filter = GeneralFilter.GeneralFilter(argv[0], 'HB')
	l_filter.listFilter(hb_list)

def print_usage(name):
        print "Usage : " + name + " <folder name> <res_list>"

if __name__ == "__main__":
        main(sys.argv[0], sys.argv[1:])
