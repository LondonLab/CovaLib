#!/usr/local/python-2.7.11/bin/python
#Written by Daniel Zaidman
#Code review by 

import sys,os,math
import subprocess
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
	if len(argv) != 6:
		print_usage(name)
		return
	
	clu = Cluster.Cluster()
	commands = []
	with open(argv[4], 'r') as f_lib:
		for line in f_lib:
			#commands.append(' '.join(['python', Paths.SCRIPTS + 'CyScan/CyScan.py'] + argv[:4] + line.split() + [argv[5], 'False']))
			subprocess.call(['python', Paths.SCRIPTS + 'CyScan/CyScan.py'] + argv[:4] + line.split() + [argv[5], 'False'])
			if argv[5] == '1' or argv[5] == '0':
				break
	'''if argv[5] == '1':
		clu.runSingle(commands[0])
	else:
		clu.runCommands(commands)'''

def print_usage(name):
	print "Usage : " + name + " <pdb_name> <receptor_chain> <residue_file Default=around xtal-lig> <xtal-lig> <libraries_file> <Rosetta+Prepare+Tarting(1)/Docking(2)/Combine(3)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
