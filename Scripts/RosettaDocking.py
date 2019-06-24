import subprocess
import sys
import re
import os
import shutil
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 1:
                print_usage(name)
                return

	treshold = [0.0, 1.5, 3.0, 4.5, 6.0, 20.0, 1000.0]
	#ARLS script - a script to create scripts
	os.system('python ' + Paths.SCRIPTS + 'ARLS/arls.py -m $ROSETTA/ --compile-tag=default.linuxgccrelease --openeye=/work/londonlab/software/openeye/ -d /home/danielza/Rosetta/main/database/ --local --clobber --cluster=BASH --njobs=1 ' + argv[0])
	os.chdir('arls_work/')
	#Applying these scripts
	os.system('./1_setup.sh')
	os.system('./2_prepack_minimize.sh')
	os.system('./3_tarball_pre.sh')
	os.system('./4_dock_bash.sh')
	os.system('./BASH.dock.sh')
	os.system('./5_concat.sh')
	os.system('./6_analyze_results.sh')
	
#os.chdir('mol2_out/')
	#os.system('python ' + Paths.SCRIPTS + 'SeperateMol2.py rec_xtal-lig.mol2')
	rmsd = []
	indices = []
	for i, line in enumerate(open('pdbs/rmsd.txt', 'r')):
		rmsd.append((str(i), float(line[:-1])))
	rmsd = sorted(rmsd, key=lambda tup: tup[1])
	candidates = []
	t = 1
	for i, pair in enumerate(rmsd):
		while pair[1] >= treshold[t]:
			t += 1
		if treshold[t - 1] < pair[1] < treshold[t]:
			#shutil.copy(pair[0], '../cand' + str(t) + '.mol2')
			indices.append((t, pair[0]))
			t += 1
			if t == len(treshold):
				break
	os.system('python ' + Paths.SCRIPTS + 'SeperateMol2.py mol2_out/rec_xtal-lig.mol2 ' + ' '.join([index[1] for index in indices]))
	for index in indices:
		shutil.copy('mols/' + index[1] + '.mol2', '../cand' + str(index[0]) + '.mol2')
		with open('mols/' + index[1] + '.mol2', 'r') as f:
			for line in f:
				if re.search('pdbs/', line):
					shutil.copy(line[:-1], '../rec' + str(index[0]) + '.pdb')
	shutil.copy('out/rec_xtal-lig_silent.out', '../silent.out')
	#shutil.copy('Dock/result/OUTDOCK', '../')
	#shutil.copy('rec.pdb', '../')
	#shutil.copy('xtal-lig.pdb', '../')
	#shutil.copy(argv[0], '../')'''
	os.chdir('../')

def print_usage(name):
        print "Usage : " + name + " <param_file>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
