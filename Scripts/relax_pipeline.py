#Written by Daniel Zaidman
#Code review by 

import subprocess
import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
import shutil
from openeye.oechem import *

def main(name, argv):
    if len(argv) < 6:
        print_usage(name)
        return
    imol2 = argv[0]
    ismi = argv[0][:-4] + 'smi'
    ipdb = argv[0][:-4] + 'pdb'
    subprocess.call(["python", "/home/danielza/CovaLib/Scripts/ChemChem/convert.py", imol2, ismi])
    subprocess.call(["python", "/home/danielza/CovaLib/Scripts/ChemChem/convert.py", imol2, ipdb])
    if len(argv) > 6:
        ismi = argv[6]
    with open(ipdb, 'r') as fpdb:
        lines = fpdb.readlines()
    with open(ipdb, 'w') as fpdb:
        for line in lines:
            if line[0] == 'H' or line[0] == 'T':
                fpdb.write(line[:17] + argv[4] + line[20:])
            else:
                fpdb.write(line)
    confs = "all_confs.mol2"
    f = open(confs, 'w')
#    subprocess.call(["cxcalc", "conformers", "-m", "250", "-f", "mol2", ismi], stdout = f)
#    subprocess.call([Paths.SCRIPTS + "rmsd.py", "-in", confs, "-ref", imol2, "-out", "moved_confs.mol2"])
    fout = open('charges.mol2', 'w')
#    fin = open('moved_confs.mol2', 'r')
    fin = open('all_confs.mol2', 'r')
    print "Im here"
#    subprocess.call([Paths.ROSETTA + "src/apps/public/ligand_docking/assign_charges.py"], stdin = fin, stdout = fout)
#    subprocess.call([Paths.ROSETTA + "scripts/python/public/molfile_to_params.py", "-n", argv[4],  "-p", argv[4], "charges.mol2"])
    subprocess.call([Paths.ROSETTA + "scripts/python/public/molfile_to_params.py", "-n", argv[4],  "-p", argv[4], "all_confs.mol2"])
    print "Im here2"
    f_conf_pdb = open(argv[4] + '_confs.pdb', 'w')
    files = []
    for i in range(1,251):
        files.append(argv[4] + "_%04d.pdb" % i)
    #Changing numbering
    with open(ipdb, 'r') as fpdb:
        lines = fpdb.readlines()
    empty_lines = 0
    for i, line in enumerate(lines):
        if not line[0] == 'H':
            empty_lines += 1
        if 'C' + argv[3] + ' ' in line:
            cov_id = i - empty_lines
            break
    print "Im here"
    if len(argv) > 6:
        min_rmsd = 'min_rmsd.mol2'
        min_pdb = 'min_rmsd.pdb'
        subprocess.call(["convert.py", min_rmsd, min_pdb])
        ipdb = min_pdb
        PDBUtils.changeMolChain(ipdb, argv[4])
        cov_name = 'C' + argv[3]
    else:
        subprocess.call(['python', Paths.SCRIPTS + 'OrderPDB.py', imol2, 'min_rmsd.mol2', ipdb])
        with open(ipdb, 'r') as fpdb:
            for i in range(cov_id + 1):
                line = fpdb.readline()
        cov_name = line[12:15]
    
    subprocess.call(["cat"] + files, stdout = f_conf_pdb)
    params_name = argv[4] + '.params'
    with open(params_name, 'a') as fparams:
        fparams.write("PDB_ROTAMERS " + argv[4] + "_confs.pdb\n")
    rparams = Relax_Params.Relax_Params(params_name, cov_name[1:])
    rparams.process()
    rparams.add_connect()
    rparams.find_Hs()
    rparams.delete_atoms()
    rparams.find_parent()
    rparams.delete_icoor()
    rparams.add_icoor()
    rparams.write_to_file('new.params')
    con_atoms = rparams.get_con_atoms()
    rparams.close()
    shutil.move('new.params', params_name)
    rec_ex = os.path.abspath(argv[1][:-4] + 'e.pdb')
    #subprocess.call([Paths.PDBUTILS + 'extract_chains_and_range.pl', '-p', argv[1], '-c', argv[5], '-o', rec_ex])
    shutil.copyfile(argv[1], rec_ex)
    rec_x = os.path.abspath(argv[1][:-4] + 'x.pdb')
    rec_f = open(rec_x , 'w')
    for line in open(rec_ex, 'r'):
        if '%3s' % argv[2] in line[23:26]:
            cov_res_name = line[17:20]
            if line[17:20] == 'CYS':
                rec_f.write(line[:17] + 'CYX' + line[20:])
            else:
                rec_f.write(line[:20] + 'X' + line[21:])
        elif 'HI' == line[17:19]:
            rec_f.write(line[:17] + 'HIS' + line[20:])
        else:
            rec_f.write(line)
    rec_f.close()
    rec_lig = 'rec_lig.pdb'
    subprocess.call(["cat", rec_x, ipdb], stdout = open(rec_lig, 'w'))
    subprocess.call([Paths.PDBUTILS + 'sequentialPdbResSeq.pl', '-pdbfile', rec_lig], stdout = open('res_num.pdb', 'w'))
    with open('res_num.pdb', 'r') as res_f:
        sum_of_res = 0
        pre_num = 0
        for line in res_f:
            if not line[0] == 'A' and not line[0] == 'H':
                continue
            tmp_num = int(line[23:26])
            if tmp_num == 1 and pre_num > 1:
                sum_of_res += pre_num
            if 'CYX' in line:
                res_num = tmp_num
            elif line[20] == 'X':
                res_num = tmp_num
            if argv[4] in line:
                lig_num = sum_of_res + 1
                break
            pre_num = tmp_num
    cst_f = open('cst', 'w')
    if cov_res_name == 'CYS':
        rec_cov_atom = 'SG'
    elif cov_res_name == 'THR':
        rec_cov_atom = 'OG1'
    lig_num = 145
    cst_f.write('AtomPair ' + cov_name + ' ' + str(lig_num) + ' ' + rec_cov_atom + ' ' + str(res_num) + ' HARMONIC 1.8 0.05\n')
    cst_f.write('Angle CB ' + str(res_num) + ' ' + rec_cov_atom + ' ' + str(res_num) + ' ' + cov_name + ' ' + str(lig_num) + ' HARMONIC 1.91 0.17\n')
    for con in con_atoms:
        con2 = con
        if con[-1] == ' ':
            con2 = con[:-1]
        cst_f.write('Angle ' + rec_cov_atom + ' ' + str(res_num) + ' ' + cov_name + ' ' + str(lig_num) + ' ' + con2  + ' ' + str(lig_num) + ' HARMONIC 1.91 0.17\n')
    cst_f.close()
    flags_f = open('relax.flags', 'w')
    flags_f.write('-extra_res_fa ' + argv[4]+ '.params\n-nstruct 50\n-packing::ex1\n-packing::ex1aro\n-packing::ex2\n-packing::extrachi_cutoff 1\n-in:file:fullatom\n-relax:fast\n-cst_fa_file cst \n-cst_fa_weight 1.0\n#-fix_disulf ss \n-relax:constrain_relax_to_start_coords\n')
    flags_f.close()
    clu = Cluster.Cluster()
    #clu.runCommandsArgs('/work/londonlab/Rosetta/main/source/bin/relax.linuxgccrelease -s ' + rec_lig + ' -native ' + rec_lig + ' -extra_res_fa /work/londonlab/Rosetta/main/database/chemical/residue_type_sets/fa_standard/residue_types/sidechain_conjugation/CYX.params @relax.flags -overwrite true -out:prefix', range(10))
    clu.runCommandsArgs('/work/londonlab/Rosetta/main/source/bin/relax.linuxgccrelease -s ' + rec_lig + ' -native ' + rec_lig + ' -extra_res_fa /work/londonlab/Rosetta/main/database/chemical/residue_type_sets/fa_standard/residue_types/sidechain_conjugation/CYX.params -extra_res_fa ../GDP.params @relax.flags -overwrite true -out:prefix', range(10))
def print_usage(name):
    print "Usage : " + name + " <mol2 file> <rec pdb file> <covalent residue index> <covalent atom number> <prefix for files> <chain in pdb> <optional - alternative smiles + covalent atom should match the conformations and not the original>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
