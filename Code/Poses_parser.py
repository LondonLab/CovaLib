class Poses_parser:
    def __init__(self,path):
        poses_f = open(path).readlines()
        self.poses_f = poses_f
        start_inds = []
        for i in range(len(poses_f)):
            if poses_f[i].startswith('##########                 Name'):
                start_inds.append(i)
        self.start_inds = start_inds
    def get_lig(self,x):
        ligand = self.poses_f[self.start_inds[x]:self.start_inds[x+1]]
        return ligand
    def get_lig_coords(self,x):
        ligand = self.get_lig(x)
        start_ind = ligand.index('@<TRIPOS>ATOM\n')+1
        end_ind = ligand.index('@<TRIPOS>BOND\n')
        lig_coords = ligand[start_ind:end_ind]
        return lig_coords
    def get_lig_bonds(self,x):
        ligand = self.get_lig(x)
        start_ind = ligand.index('@<TRIPOS>BOND\n')+1
        lig_bonds = ligand[start_ind:]
        return lig_bonds
    def get_lig_properties(self,x):
        ligand = self.get_lig(x) 
        name = ligand[0].split()[2]
        num_of_atoms = ligand[24].split()[4]
        charge = ligand[22].split()[3]
        return name, num_of_atoms, charge
    def find_lig_don_acc(self,x):
        lig_donors = []
        lig_acceptors = []
        coords = self.get_lig_coords(x)
        bonds = self.get_lig_bonds(x)
        ligO = []
        ligC = []
        ligN = []
        ligH = []
        ligS = []
        ligP = []
        ligHal = []
        ligUKN = []
        for atom in coords:
            sp_atom = atom.split()
            if sp_atom[1].startswith('O'): ligO.append(sp_atom[0])
            elif sp_atom[1].startswith('C'): ligC.append(sp_atom[0])
            elif sp_atom[1].startswith('N'): ligN.append(sp_atom[0])
            elif sp_atom[1].startswith('H'): ligH.append(sp_atom[0])
            elif sp_atom[1].startswith('S'): ligS.append(sp_atom[0])
            elif sp_atom[1].startswith('P'): ligP.append(sp_atom[0])
            elif sp_atom[1].startswith('F') or sp_atom[1].startswith('Cl'): ligHal.append(sp_atom[0])
            else:ligUKN.append(sp_atom[0])
        for ind in ligH:
            for bond in bonds:
                bond = bond.split()
                if (bond[2] == ind) and (bond[1] not in ligC+ligUKN):
                    lig_donors.append(coords[int(ind)-1].split()[2:5])
        for ind in ligO+ligS:
            lig_acceptors.append(coords[int(ind)-1].split()[2:5])
        for ind in ligN+ligP:
            num_bonds = []
            for bond in bonds:
                bond = bond.split()
                if bond[2] == ind: num_bonds.append(bond)
            if len(num_bonds) <= 3: lig_acceptors.append(coords[int(ind)-1].split()[2:5])
        return lig_donors, lig_acceptors
    
    
class rec:
    def __init__(self,path):
        rec_f = open(path).readlines()
        self.rec_f = rec_f
    def get_rec_don_acc(self):
        rec_donors = []
        rec_acceptors = []
        rec_others = []
        for line in self.rec_f:
            atom = line[12:16].strip()
            res = line[17:20]
            if atom.startswith('H'):
                if 'HG  CYS A 113' in line: 
                    continue
                else:
                    rec_donors.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
            elif (atom.startswith('O')) or (atom.startswith('S')):
                if 'SG  CYS A 113' in line:
                    continue
                else: 
                    rec_acceptors.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
            else: rec_others.append([float(line[30:38]),float(line[38:47]),float(line[47:56])])
        return rec_donors, rec_acceptors, rec_others

