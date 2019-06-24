import sys,os,math
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 4 and not len(argv) == 5:
                print_usage(name)
                return
	
	if not os.path.exists(argv[3]):
		os.mkdir(argv[3])
	cluster = Cluster.Cluster()
	lines = []
	for i in range(500):
		lines.append(' '.join([argv[0], argv[1], argv[2] + str(i) + '.ism', argv[3] + '/' + str(i) + '_1.ism']))
		if len(argv) == 5 and (argv[4] == 'true' or argv[4] == 'True'):
			lines.append(' '.join([argv[0], argv[2] + str(i) + '.ism', argv[1], argv[3] + '/' + str(i) + '_2.ism']))
	cluster.runCommandsArgs('python ' + os.environ["SCRIPTS"] + '/RDKit/bimol_multireactions.py', lines)

def print_usage(name):
        print "Usage : " + name + " <bireaction_file> <infile1> <infolder2> <outfolder> <two_ways (default=false)>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
