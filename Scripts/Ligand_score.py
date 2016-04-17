from openeye.oechem import *
import sys,os,math
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *

def get_purch(lig_name):#very slow!!!
    sys.path.append("/work/londonlab/git_dock/DOCK/analysis")
    import zincapi
    zinc = zincapi.ZINCAPI()
    zinc_id = 'ZINC'+lig_name[3:14]
    lig = zinc.substances.get(zinc_id, fields=('zinc_id', 'purchasability'))
    purch_log = int(lig.purchasability == 'For_Sale')
    return purch_log

def get_purch2(lig_name):
    import re
    st = re.search('[1-9]',lig_name).start()
    zinc_id = lig_name[st:14]
    pre_cmd = 'curl http://zinc15.docking.org/substances.txt:zinc_id+smiles+purchasability -F zinc_id-in='+zinc_id+' -F count=all'
    cmd = pre_cmd.split()
    from subprocess import Popen, PIPE
    output,error = Popen(cmd,stdout = PIPE, stderr= PIPE).communicate()
    if len(output.split())==3:
        return output.split()[2]
    else:
        return 'UNKNOWN'

def charged_smiles(smiles):
    smi_f = open('./tmp4.smi','w')
    smi_f.write(smiles)
    smi_f.flush()
    cmd = '/work/londonlab/software/ChemAxon/MarvinBeans/bin/cxcalc majorms -H 7 tmp4.smi'
    from subprocess import Popen, PIPE
    output,error = Popen(cmd.split(),stdout = PIPE, stderr= PIPE).communicate()
    os.remove('./tmp4.smi')
    if len(output.split('\t')) == 3:
        smiles7 = output.strip().split('\t')[2]
    else: smiles7 = 'no_ch_smi'
    return smiles7
    

def check_for_tzvi(smiles):#checks also for double reactivity
    ch_smiles = charged_smiles(smiles)
    if ch_smiles == 'no_ch_smi': return 'no_ch_smi'
    else:
        mol = OEGraphMol()
        OESmilesToMol(mol, ch_smiles)
        matches = 0
        for pat in ['[$([!-0!-1!-2!-3!-4]~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~*~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~*~*~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~*~*~*~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~*~*~*~*~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~*~*~*~*~*~*~[!+0!+1!+2!+3!+4]),$([!-0!-1!-2!-3!-4]~*~*~*~*~*~*~*~*~*~[!+0!+1!+2!+3!+4])]','[C;H2][Cl,Br,I]']:
            ss = OESubSearch(pat)
            OEPrepareSearch(mol, ss)
            for count, match in enumerate(ss.Match(mol)):
                matches += count+1
        if matches == 0: return 'good'
        else: return 'smart-fail'

def check_C_degree(smiles):
    if 'C[SiH3]' in smiles: return '1'
    else: return '2'

def dist (a1,a2):
    a1 = [float(x) for x in a1]
    a2 = [float(x) for x in a2] 
    return math.sqrt((a1[0]-a2[0])*(a1[0]-a2[0])+(a1[1]-a2[1])*(a1[1]-a2[1])+(a1[2]-a2[2])*(a1[2]-a2[2]))

def count_bonds(lig,rec,rec_oths):#,LEN_HYD_BOND):
    LEN_HYD_BOND = 2.5
    num_hyd_bonds = 0
    num_unsut = 0
    num_unsut_buried = 0
    num_bonded_lig_atms = 0
    num_bonded_rec_atms = 0
    for lig_atom in lig:
        bond_per_atom = 0
        for rec_atom in rec:
            bond_len = dist(lig_atom,rec_atom)
            if bond_len<LEN_HYD_BOND:
#                print [lig_atom,rec_atom,bond_len]
                num_hyd_bonds +=1
                bond_per_atom +=1
        if bond_per_atom == 0:
            num_unsut +=1
            num_neighbors = 0
            for oth in rec_oths:
                bond_len = dist(lig_atom,oth)
                if bond_len < LEN_HYD_BOND+2:
                     num_neighbors +=1
            if num_neighbors > 1:
                num_unsut_buried +=1
        else: num_bonded_lig_atms += 1
    return num_hyd_bonds, num_unsut, num_unsut_buried, num_bonded_lig_atms 

def main(name, argv):
    if (len(argv) != 1):
        print_usage(name)
        return
    path = os.getcwd()
    PDB_list = open(path+'/'+argv[0],'r').readlines()  
    score_name = 'unsubstituted-acrylamides.lead'
#    outfile = open(path+'/'+score_name+'ligand_score.txt','a')
    PyUtils.create_folder(score_name)
    score_path = path+'/'+score_name+'/'
    for i in range(len(PDB_list)):
        PDBid = PDB_list[i].split()[0]
        print PDBid
        rec_path = path+'/'+PDBid+'/working/rec.crg.pdb'
        rec_f = Poses_parser.rec(rec_path)
        rec_dons, rec_accs, rec_oths, rec_all = rec_f.get_rec_don_acc()
        outfile_local = open(score_path+'/'+PDBid+'_ligand_score.txt','a')
        mol_path = path+'/'+PDBid+'/run.unsubstituted-acrylamides.lead/poses.mol2'
        poses_f = Poses_parser.Poses_parser(mol_path)
        len_poses = poses_f.get_len_poses()
        for x in range(len_poses-1):
            print PDBid+' '+str(x)
            lig_name,size,charge = poses_f.get_lig_properties(x)
            lig_purch = get_purch2(lig_name)
#            lig_purch = 'purch'
            lig_dons,lig_accs = poses_f.find_lig_don_acc(x)
            tot_hyd_bonds = 0
            tot_unsut = 0
            tot_unsut_buried = 0
            num_bonded_lig_atms = 0
            cb = count_bonds(lig_dons,rec_accs,rec_all)
            tot_hyd_bonds += cb[0]
            tot_unsut += cb[1]
            tot_unsut_buried += cb[2]
            num_bonded_lig_atms += cb[3]
            cb = count_bonds(lig_accs,rec_dons,rec_all)
            tot_hyd_bonds += cb[0]
            tot_unsut += cb[1]
            tot_unsut_buried += cb[2]
            num_bonded_lig_atms += cb[3]
            smiles = poses_f.get_smiles(x)
            tzvi = check_for_tzvi(smiles)
            deg = check_C_degree(smiles)
            energies = poses_f.get_energies(x)
            energies = ' '.join(energies)
            tot_num_clushes = 0
            clush_score = '1'
            cb = count_bonds(lig_dons,rec_dons,rec_all)
            tot_num_clushes += cb[0]
            lig_coords = poses_f.get_lig_coords(x)
            lig_dists_to_rec = 0
            for lig_atom in lig_coords:
                lig_atom = lig_atom.split()[2:5]
                atom_dists_to_rec = 0
                for rec_atom in rec_all:
                    dist_to_rec = dist(lig_atom,rec_atom)
                    atom_dists_to_rec += (dist_to_rec)**2
                mean_atom_dist_to_rec = (atom_dists_to_rec/len(rec_all))**0.5
                lig_dists_to_rec += mean_atom_dist_to_rec
            mean_lig_dist_to_rec = str(lig_dists_to_rec/len(lig_coords))
            if tot_num_clushes != 0:
                clush_score = 'clush';
            output = ' '.join([PDBid,str(x+1),lig_name,size,charge,str(tot_hyd_bonds),str(tot_unsut),str(tot_unsut_buried),str(num_bonded_lig_atms),lig_purch,tzvi,deg,energies,clush_score,mean_lig_dist_to_rec])
#            outfile.write(output+'\n')
            outfile_local.write(output+'\n')

def print_usage(name):
    print "Usage : " + name + " <PDB_list_file>"


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])

