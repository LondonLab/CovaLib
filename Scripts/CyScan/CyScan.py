#Written by Daniel Zaidman
#Code review by 

import sys,os,math
sys.path.append(os.environ["COVALIB"])
from Code import *
import subprocess
import shutil
import fileinput

def main(name, argv):
	if not len(argv) == 7 and not len(argv) == 8:
		print_usage(name)
		return
	clu = Cluster.Cluster()
	kinase = False
	if len(argv) == 7 or (len(argv) == 8 and argv[-1] == 'True'):
		kinase = True
	#extract chain
	renum = argv[0][:-4] + '_renum.pdb'
        subprocess.call([Paths.PDBUTILS + 'extract_chains_and_range.pl', '-p', argv[0], '-c', argv[1], '-o', renum])
	#get pocket residues
	if argv[2] == 'Default':
		with open('res_nums', 'w') as f_res:
                        subprocess.call(['python', Paths.SCRIPTS + 'expand_selection.py', renum, argv[3]], stdout=f_res)
                        print ' '.join(['python', Paths.SCRIPTS + 'expand_selection.py', argv[0], argv[3]])
		argv[2] = 'res_nums'
	with open(argv[2], 'r') as f:
		residues = f.readline().split(',')
		if kinase:
			true_res = f.readline()[:-1]
	if residues[-1][-1] == '\n':
		residues[-1] = residues[-1][:-1]
	#initializations
	commands = []
	score = []
	run_mode = argv[6]
	#check whether to tart or not
	if not os.path.exists('kinase_params') and not os.path.exists('tart_params'):
		tart_bool = False
	else:
		tart_bool = True
	if os.path.exists('dirlist'):
		dir_f = open('dirlist', 'a')
	else:
		dir_f = open('dirlist', 'w')
	#action over all cysteine positions
	for res in residues:
		folder = 'CYS' + res + '/'
		PyUtils.create_folder(folder)
		#rosettaScript - mutate to cys and local repack
		if run_mode == '0':
			subprocess.call([Paths.ROSETTA + "/bin/rosetta_scripts.default.linuxgccrelease", "-s", renum, "-parser:protocol", Paths.SCRIPTS + "CyScan/Mutate.xml", "-out:prefix", "CYS_" + res + "_", "-overwrite", "-parser:script_vars", "pos=" + res + argv[1], '@' + Paths.SCRIPTS + 'CyScan/relax.flags'])
			orig_folder = folder + 'Rot0/'
			#dir_f.write(orig_folder + '\n')   
			PyUtils.create_folder(orig_folder)
			shutil.move('CYS_' + res + '_' + renum[:-4] + '_0001.pdb', orig_folder + 'rec.pdb')
			shutil.move('CYS_' + res + '_score.sc', orig_folder + 'score.sc')
			shutil.copy(argv[3], orig_folder)
			PYMOLUtils.pymol_mutate(renum, argv[1], res, 1)
			for state in range(1, 4):
				state_file = 'rec_' + res + '_' + str(state) + '.pdb'
				if not os.path.exists(state_file):
					continue
				rot_folder = folder + 'Rot' + str(state) + '/'
				dir_f.write(rot_folder + '\n')
				PyUtils.create_folder(rot_folder)
				shutil.move(state_file, rot_folder + 'rot.pdb')
				shutil.copy(argv[3], rot_folder)
				os.chdir(rot_folder)
				subprocess.call([Paths.ROSETTA + "/bin/rosetta_scripts.default.linuxgccrelease", "-s", 'rot.pdb', "-parser:protocol", Paths.SCRIPTS + "CyScan/Repack.xml", "-out:prefix", "CYS_" + res + "_", "-overwrite", "-parser:script_vars", "pos=" + res + argv[1], '@' + Paths.SCRIPTS + 'CyScan/relax.flags'])
				#put each one in its own folder
				shutil.move('CYS_' + res + '_rot_0001.pdb', 'rec.pdb')
				shutil.move('CYS_' + res + '_score.sc', 'score.sc')
				os.chdir('../..')
		os.chdir(folder)
		for rot in os.listdir('./')[1:]:
			os.chdir(rot)
			#Preparing and tarting (if tart file exists)
			if run_mode == '1':
				#Only prepare
				if not tart_bool:
					commands.append(' '.join(['python', Paths.SCRIPTS + 'Prepare.py', 'rec.pdb', 'xtal-lig.pdb', 'CYS', res, 'HG']))
				#reading the tarting files and changing the charges
				else:
					if kinase:
						with open('../../kinase_params', 'r') as f_tart:
							change_charges(f_tart.readline().split(), [('H', 0), ('O', -0.4)] ,1)
							change_charges(f_tart.readline().split(), [('H', 0.8), ('O', -0.4)] ,2)
					else:
						with open('../../tart_params', 'r') as f_tart:
							for i, line in enumerate(f_tart):
								spl = line.split()
								res_list = spl[:3]
								spl = spl[3:]
								t_atoms = []
								for j in range(len(spl)/2):
									t_atoms.append((spl[j * 2], float(spl[j * 2 + 1])))
								change_charges(res_list, t_atoms, i + 1)
					#Preparing with new charges
					commands.append(' '.join(['python', Paths.SCRIPTS + 'Prepare.py', 'rec.pdb', 'xtal-lig.pdb', 'CYS', res, 'HG', 'True']))
			#Only Docking
			if run_mode == '2':
				commands.append(' '.join(['python', Paths.SCRIPTS + 'DOCKovalentTask.py', argv[5], argv[4], 'True']))
			#Combine and get rank
			if run_mode == '3':
				subprocess.call(['python', Paths.SCRIPTS + 'Combine.py', argv[5], 'False'])
				os.chdir(argv[5])
				subprocess.call(['python', Paths.SCRIPTS + 'FilterList.py', '1', './', 'BIG_MOLS', 'True'])
				shutil.copy('BIG_MOLS/poses.mol2', './')
				shutil.copy('BIG_MOLS/extract_all.sort.uniq.txt', './')
				os.chdir('../')
				if tart_bool:
					res_list = []
					if kinase:
						f_tart = open('../../kinase_params', 'r')
					else:
						f_tart = open('../../tart_params', 'r')
					for line in f_tart:
						res_list.append(line.split()[2])
					f_tart.close()
					commands.append(' '.join(['python', Paths.SCRIPTS + 'HBondsFilter.py', argv[5]] + res_list))
					print (' '.join(['python', Paths.SCRIPTS + 'HBondsFilter.py', argv[5]] + res_list))
				else:
					commands.append(' '.join(['python', Paths.SCRIPTS + 'HBondsFilter.py', argv[5]] + residues))
				'''with open('Docking/extract_all.sort.uniq.txt', 'r') as f_score:
					if kinase:	
						for line in f_score:
							score.append((float(line.split()[-1]), res))
					else:
						with open('top500', 'w') as f_res:
							f_res.write(folder)
							for line in f_score:
								f_res.write(line.split()[-1] + '\n')'''
			os.chdir('../')
		os.chdir('../')
	dir_f.close()
	if kinase and run_mode == '3':
		with open('res_scores', 'w') as res_f:
			res_f.write(str(sorted(score)) + '\n')
			subprocess.call(["python", Paths.SCRIPTS + "/rmsd.py", "-ref", "xtal-lig.pdb", "-in", "CYS" + true_res + "/Docking/poses.mol2", "-overlay", "false"])
			res_f.write('Rank of True Cysteine is: ' + str([x[1] for x in sorted(score)].index(true_res) + 1) + ' out of ' + str(len(residues)) + '\n')
			with open('rmsd.txt', 'r') as f_rmsd:
				rmsd = f_rmsd.readline()
			res_f.write('Rmsd is: ' + rmsd)
		os.remove('rmsd.txt')
	if run_mode == '1' or run_mode == '2' or run_mode == '3':
		clu.runDirCommands('dirlist', commands)

def change_charges(list_kin, t_atoms, ind):
	shutil.copy('rec.pdb', './nontart.pdb')
	if ind == 1:
		shutil.copy(Paths.DOCKBASE + '/proteins/defaults/prot.table.ambcrg.ambH', './')
		shutil.copy(Paths.DOCKBASE + '/proteins/defaults/amb.crg.oxt', './')
	shutil.copy('prot.table.ambcrg.ambH', './old.prot')
	shutil.copy('amb.crg.oxt', './old.amb')
	line_kin = ' '.join(list_kin)

	#Change the rec.crg.pdb                                                                                                                                                                                                       
	rec_new = open('rec.pdb', 'w')
	with open('nontart.pdb') as f_kin:
		for line in f_kin:
			if ' ' + list_kin[2] + '     ' in line and not 'CYS' in line:
				rec_new.write(line[:17] + 'RE' + str(ind) + line[20:])
			else:
				rec_new.write(line)
	rec_new.close()
	os.remove('nontart.pdb')

	#Chage prot
	prot_new = open('prot.table.ambcrg.ambH', 'w')
	new_lines =[]
	with open('old.prot', 'r') as f_prot:
		hng_res = False
		for line in f_prot:
			if ' ' + list_kin[0] + ' ' in line:
				hng_res = True
				new_lines.append(line[:7] + 'RE' + str(ind) + line[10:])
			elif hng_res:
				hng_res = False
				for new_line in new_lines:
					tarted = False
					for t_atom in t_atoms:
						if t_atom[0] + ' ' in new_line:
							prot_new.write(new_line[:17] + '%6s' % "{0:.3f}".format(float(new_line[17:23]) + t_atom[1]) + new_line[23:])
							tarted = True
					if not tarted:
						prot_new.write(new_line)
			prot_new.write(line)
	prot_new.close()
	os.remove('old.prot')

	#Change amb
	amb_new = open('amb.crg.oxt', 'w')
        new_lines =[]
        with open('old.amb', 'r') as f_amb:
                hng_res = False
                for line in f_amb:
                        if ' ' + list_kin[0].lower() + ' ' in line:
                                hng_res = True
                                new_lines.append(line[:6] + 're' + str(ind) + line[9:])
                        elif hng_res:
                                hng_res = False
                                for new_line in new_lines:
                                        tarted = False
					for t_atom in t_atoms:
						if t_atom[0] + ' ' in new_line:
							amb_new.write(new_line[:16] + '%6s' % "{0:.3f}".format(float(new_line[16:22]) + t_atom[1]) + new_line[22:])
							tarted = True
					if not tarted:
                                                amb_new.write(new_line)
                        amb_new.write(line)
        amb_new.close()
	os.remove('old.amb')
				
def print_usage(name):
	print "Usage : " + name + " <pdb_name> <receptor_chain> <residue_file> <xtal-lig> <docking_library> <folder_name> <Rosetta+Prepare+Tarting(1)/Docking(2)/Combine(3)> <Kinase_run (default=True)>"

if __name__ == "__main__":
	main(sys.argv[0], sys.argv[1:])
