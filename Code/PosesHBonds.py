#Written by Daniel Zaidman
#Code review by 

import shutil
import subprocess
import os
import sys
import Paths
import PyUtils
import Cluster
import PYMOLUtils

class PosesHBonds:
    def __init__(self, folder_name, res_list):
        self.res_list = res_list
	self.folder = os.getcwd() + "/"
        self.name = self.folder + folder_name + "/"
        self.rec_lines = []
        self.counters = []
        with open('rec.pdb', 'r') as f_rec:
            for line in f_rec:
                if 'ATOM' in line:
                    self.rec_lines.append(line)
        os.chdir(self.name)
        self.seperate_poses()
        self.poses2pdb()
        os.chdir("../")
    #Inner functions
    def seperate_poses(self):
        subprocess.call(['python', Paths.SCRIPTS + 'SeperatePoses.py', 'poses.mol2'])
    def poses2pdb(self):
        PyUtils.create_folder('recs')
        os.chdir('poses')
        for k in range(1, len(os.listdir(os.getcwd())) + 1):
            i = str(k) + '.mol2'
            surface = PYMOLUtils.get_surface_area(i)
            with open(i, 'r') as f_mol:
                for line in f_mol:
                    if 'SMILES' in line:
                        smile_line = line.split()[2]
                    if 'heavy atom count' in line:
                        heavy_atoms = int(line.split()[-1])
                        break
            if surface < 200 or surface / heavy_atoms < 14.5:
                self.counters.append(0)
                continue
            if '[N+](=O)[O-]' in smile_line or smile_line.count('N') + smile_line.count('O') + smile_line.count('n') + smile_line.count('o') > 4:
                self.counters.append(0)
                continue
            pdb_pose = '../recs/' + i[:-4] + 'pdb'
            subprocess.call(['convert.py', i, pdb_pose])
            hetatm = []
            with open(pdb_pose, 'r') as f_pdb:
                for line in f_pdb:
                    if 'HETATM' in line:
                        hetatm.append(line[:23] + ' -1' + line[26:])
            rec_pose = '../recs/rec_' + i[:-4] + 'pdb'
            with open(rec_pose, 'w') as f_rec:
                for line in hetatm:
                    f_rec.write(line)
                for line in self.rec_lines:
                    f_rec.write(line)
            sub_command = []
            for res_l in self.res_list:
                sub_command.append('-seed_residue')
                sub_command.append(str(res_l))
            subprocess.call(['python', Paths.SCRIPTS + 'HBonanza.py', '-trajectory_filename', rec_pose, '-hydrogen_bond_distance_cutoff', '3.0', '-hydrogen_bond_angle_cutoff', '30', '-seed_residue', '-1'] + sub_command + ['-just_immediate_connections', 'true'], stdout=open(os.devnull, 'w'))
            os.remove(rec_pose + '.average_hbonds')
            os.remove(rec_pose + '.frame_by_frame_hbonds.csv')
            if os.path.isfile(rec_pose + '.hbond_averages_in_occupancy_column.pdb'):
                os.remove(rec_pose + '.hbond_averages_in_occupancy_column.pdb')
                counter = self.countHbonds(rec_pose + '.HBonds')
            else:
                counter = 0
            self.counters.append(counter)
            os.remove(rec_pose)
        os.chdir('../')
        shutil.rmtree('recs')
        shutil.rmtree('poses')
    def countHbonds(self, hb_file):
        counter = 0
        with open(hb_file, 'r') as hb_f:
            for line in hb_f:
                if not line[0] == 'N' and line.split()[1] in self.res_list:
                    counter += 1
        return counter
    def getList(self):
        return [a[0] for a in sorted([(i, e) for i, e in enumerate(self.counters) if e != 0], key=lambda tup: tup[1], reverse = True)]
