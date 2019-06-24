import subprocess
import sys
import os
import shutil
sys.path.append(os.environ["COVALIB"])
from Code import *

def main(name, argv):
        if not len(argv) == 4:
                print_usage(name)
                return

	num_save = '2000'
	num_extract = '10000'
	num_bump = '20.0'
	argv[0] += '.pdb'
	treshold = [0.0, 1.5, 3.0, 4.5, 6.0, 20.0, 1000.0]
	PYMOLUtils.seperate_rec_lig(*argv)
	rec = 'rec.pdb'
	lig = 'xtal-lig.pdb'
	smiles = argv[1] + '.ism'
	mol2 = argv[1] + '.mol2'
	os.system('convert.py ' + lig + ' ' + smiles)
	os.system('convert.py ' + lig + ' ' + mol2)
	with open(smiles, 'r+') as f:
		line = f.readline()
		f.seek(0)
		f.write(line[:-1] + '\t' + argv[1] + '\n')
	os.system('/work/londonlab/git_dock/DOCK/ligand/generate/build_smiles_ligand.sh ' + smiles)
	os.system('/work/londonlab/git_dock/DOCK/proteins/blastermaster/blastermaster.py')
	#shutil.rmtree(argv[1] + '/')
	indock = []
	for line in open('INDOCK', 'r'):
		if 'number_save' in line:
			indock.append(line[:-2] + num_save + '\n')
#		elif 'bump_' in line:
#			indock.append(line[:-5] + num_bump + '\n')
		else:
			indock.append(line)
	with open('INDOCK', 'w') as f:
		for line in indock:
			f.write(line)
	compound = os.path.abspath(argv[1] + '.db2.gz')[5:]
	print compound
	os.system('python ' + os.environ["SCRIPTS"] + '/DOCKovalentTask.py Dock ' + compound)
	os.chdir('Dock/')
	os.mkdir('result')
	shutil.move('OUTDOCK', 'result')
	shutil.move('test.mol2.gz', 'result')
	with open('dirlist', 'w') as f:
		f.write('result')
	os.system(Paths.DOCKBASE + 'analysis/extract_all.py --done')
	os.system(Paths.DOCKBASE + 'analysis/getposes.py -x ' + num_extract)
	os.chdir('../')
	#os.system('python ' + Paths.SCRIPTS + 'SeperatePoses.py Dock/poses.mol2')
	#mols = ['poses/' + f for f in os.listdir('poses')]
	rmsd = []
	indices = []
	os.system(Paths.SCRIPTS + 'rmsd.py -ref ' + mol2 + ' -in Dock/poses.mol2 -overlay false')
	for i, line in enumerate(open('rmsd.txt', 'r')):
		rmsd.append((str(i), float(line[:-1])))
	#for mol in mols:
	#	os.system(Paths.SCRIPTS + 'rmsd.py -ref ' + mol2 + ' -in ' + mol + ' -overlay false')
	#	with open('rmsd.txt', 'r') as f:
	#		rmsd.append((mol, float(f.readline()[:-1])))
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
	os.system('python ' + Paths.SCRIPTS + 'SeperatePoses.py Dock/poses.mol2 ' + ' '.join([index[1] for index in indices]))
	with open('../sum_cand.txt', 'w') as f:
		for index in indices:
			shutil.copy('poses/' + index[1] + '.mol2', '../cand' + str(index[0]) + '.mol2')
			f.write(str(index) + '\n')
	shutil.copy('Dock/result/OUTDOCK', '../')
	shutil.copy('rec.pdb', '../')
	shutil.copy('xtal-lig.pdb', '../')
	#shutil.copy(argv[0], '../')

def print_usage(name):
        print "Usage : " + name + " <pdb_file> <lig_name> <lig_chain> <lig_res_num>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
