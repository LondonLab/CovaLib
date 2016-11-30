import os
import PyUtils
import subprocess
import Bio.PDB as bp

def DownloadPDBs(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        PyUtils.create_folder(os.getcwd()+"/"+PDBid)
        os.chdir(PDBid)
        cmd = ["/work/londonlab/scripts/pdbUtil/getPdb.pl"+" -id "+PDBid]
        subprocess.call(cmd,shell=True)
        os.chdir("..")

def rec(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        os.chdir(PDBid)
        subprocess.call(["/work/londonlab/scripts/pdbUtil/extract_chains_and_range.pl -p "+PDBid.lower()+".pdb -c "+PDB_list[i].split()[1]+" -o rec.pdb"],shell=True)
        os.chdir("..")

def lig(PDB_list_file):
    PDB_list = open(os.getcwd()+'/'+PDB_list_file,'r').readlines()
    for i in range(len(PDB_list)):
        sp_PDB = PDB_list[i].split()
        PDBid = sp_PDB[0]  
        os.chdir(PDBid)
        PDBf_name = PDBid.lower()+".pdb"
        PDBf = open(PDBf_name).readlines()
        lig_f = open(os.getcwd()+'/xtal-lig.pdb','w')
        for line in PDBf:
            if line.startswith('HETATM'):
                sp_line = line.split()
                if len(sp_line) == 12:
                    if sp_line[3] == sp_PDB[2] and sp_line[4] == sp_PDB[1] and sp_line[5] == sp_PDB[3]:
                        lig_f.write(line)
                if len(sp_line) == 11:
                    if sp_line[3] == sp_PDB[2] and sp_line[4][0:1] == sp_PDB[1] and sp_line[4][2:] == sp_PDB[3]:
                        lig_f.write(line)
        lig_f.flush()
        os.chdir("..")
        
def count_heavy_atom(pdb_path, name = "rec"):
    """reads the input pdb as a structre object from BioPython"""
    parser = bp.PDBParser()
    structure = parser.get_structure(name, pdb_path)
    return len( [atm for atm in structure.get_atoms() if atm.element is not 'H']) 

def changeMolChain(pdb_file, new_chain):
    with open(pdb_file, 'r') as pfile:
        lines = pfile.readlines()
    with open(pdb_file, 'w') as pfile:
        for line in lines:
            if line[0] == 'H':
                pfile.write(line[:17] + new_chain + line[20:])

def alignPDB(ref, file_list):
    pdb_parser = bp.PDBParser(QUIET = True)
    io = bp.PDBIO()
    ref_structure = pdb_parser.get_structure("reference", ref)
    ref_atoms = []
    ref_model = ref_structure[0]
    for ref_chain in ref_model:
        for ref_res in ref_chain:
            ref_atoms.append(ref_res['CA'])
    super_imposer = bp.Superimposer()
    with open(file_list, 'r') as f_pdb:
        for line in f_pdb:
            sample_structure = pdb_parser.get_structure("sample", line[:-1] + '.pdb')
            sample_atoms = []
            for sample_chain in sample_structure[0]:
                for sample_res in sample_chain:
                    sample_atoms.append(sample_res['CA'])
            super_imposer.set_atoms(ref_atoms, sample_atoms)
            super_imposer.apply(sample_structure.get_atoms())
            io.set_structure(sample_structure) 
            io.save(line[:-1] + 'aligned.pdb')

def expand(ref, mol, dist = 4.0):
    pdb_parser = bp.PDBParser(QUIET = True)
    io = bp.PDBIO()
    ref_structure = pdb_parser.get_structure("reference", ref)
    mol_structure = pdb_parser.get_structure("mol", mol)
    mol_atoms = mol_structure.get_atoms()
    residues = ref_structure.get_residues()
    res_list = []
    for res in residues:
        check = False
        for atom in res:
            if check:
                break
            for atom2 in mol_structure.get_atoms():
                if atom - atom2 <= dist and len(str(res).split()[2].split('=')[1]) == 0:
                    res_list.append(str(res).split()[3].split('=')[1])
                    check = True
                    break
    return res_list
