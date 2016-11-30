import subprocess
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def main(name, argv):
        if(not len(argv) == 1):
                print_usage(name)
                return
	PyUtils.create_folder('poses')
	i = 0
	j = 1
	inside = False
        for line in open(argv[0], 'r'):
		if not(inside) and line[0] == '#':
			i += 1
			inside = True
			#poses_f = open('poses/' + line[47:-3]  + '.mol2', 'w')
			poses_f = open('poses/' + str(j) + '.mol2', 'w')
			j += 1
		if not line[0] == '#':
			inside = False
		poses_f.write(line)

def print_usage(name):
        print "Usage : " + name + " <poses file name>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
