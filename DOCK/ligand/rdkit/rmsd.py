import rdkit.Chem as rdk
import rdkit.Chem.AllChem as chm
import rdkit.Geometry.rdGeometry as gt
from optparse import OptionParser
import math 
import networkx as nx
import networkx.algorithms.isomorphism as iso
import os
from RDkit_GenConf import *

def rdkMolToNetworkxGraph(mol):
    G = nx.Graph()
    for a in mol.GetAtoms():
        G.add_node(a.GetIdx())
    for b in mol.GetBonds():
        G.add_edge(b.GetBeginAtomIdx(),b.GetEndAtomIdx())
    return G

def getGraphIsoIter(mol,ref):
    M = rdkMolToNetworkxGraph(mol)
    R = rdkMolToNetworkxGraph(ref)
    GM = iso.GraphMatcher(M,R)
    GM.is_isomorphic()
    return GM.isomorphisms_iter()


def getRmsdImmobile(prbMol, refMol,atomDic,prbConfId = 0, refConfId = 0):
    refConf = refMol.GetConformer(refConfId)
    prbConf = prbMol.GetConformer(prbConfId)  
    atomMap = []
    for k,v in atomDic.iteritems():
        atomMap.append([k,v])
    #print '***********'
    #print atomMap
    sqDist = 0.0
    for pair in atomMap:
        d = prbConf.GetAtomPosition(pair[0]).Distance(refConf.GetAtomPosition(pair[1]))
        #print pair[0],pair[1],d
        sqDist += d*d
    sqDist /= float(len(atomMap))
    return math.sqrt(sqDist)

def best_rmsd_firstConf(file_mol,file_ref):
    mol = rdk.MolFromMol2File(file_mol)
    ref = rdk.MolFromMol2File(file_ref)

    bestRmsd = None
    iso_matches_iter = getGraphIsoIter(mol,ref)
    for m in iso_matches_iter:
        rmsd = getRmsdImmobile(mol,ref,m)
        if bestRmsd is None or rmsd<bestRmsd:
            bestRmsd = rmsd
    return bestRmsd

def best_rmsd_firstConfFromMol(mol,ref):
    bestRmsd = None
    iso_matches_iter = getGraphIsoIter(mol,ref)
    for m in iso_matches_iter:
        rmsd = getRmsdImmobile(mol,ref,m)
        if bestRmsd is None or rmsd<bestRmsd:
            bestRmsd = rmsd
    return bestRmsd
    
def remove_SiH3(mol):
    atoms2remove = []
    si_a = None
    for a in mol.GetAtoms():
        if a.GetSymbol()=='Si':
            si_a = a
            break
    atoms2remove.append(si_a.GetIdx())
    for a in si_a.GetNeighbors():
        if a.GetSymbol()=='H':
            atoms2remove.append(a.GetIdx())
    atoms2remove.sort(reverse=True)

    em = rdk.EditableMol(mol)
    for i in atoms2remove:
        em.RemoveAtom(i)

    return em.GetMol()

def best_rmsd_tmp_conf(dir_tmp_conf,file_ref):
    best_rmsd = None
    best_f = None
    for f in os.listdir(dir_tmp_conf):
     if os.path.isfile(f) and f.startswith('c_') and f.endswith('.mol2'):
      mol = remove_SiH3(rdk.MolFromMol2File(f))
      ref = rdk.MolFromMol2File(file_ref)
 
      conf_bestRmsd = None
      iso_matches_iter = getGraphIsoIter(mol,ref)
      for i,m in enumerate(iso_matches_iter):
        atomMap = []
        for k,v in m.iteritems():
            atomMap.append([k,v])
       
        rmsd = chm.AlignMol(mol,ref,0,0,atomMap)
	w = rdk.PDBWriter(str(i)+f.replace('.mol2','.pdb'))
	w.write(mol)
	w.close()

        if conf_bestRmsd is None or rmsd<conf_bestRmsd:
            conf_bestRmsd = rmsd

      print f,conf_bestRmsd
      if best_rmsd is None or conf_bestRmsd<best_rmsd:
       best_f = f
       best_rmsd = conf_bestRmsd

    return best_rmsd,best_f

def alignBySiH3Core(file_mol,file_ref):
    mol = rdk.MolFromMol2File(file_mol)
    ref = rdk.MolFromMol2File(file_ref)
    mol_core,c_m = findCore(mol)
    ref_core,c_r = findCore(ref)
    print mol_core,ref_core  
    conf_bestRmsd = None
    iso_matches_iter = getGraphIsoIter(mol_core,ref_core)
    for i,m in enumerate(iso_matches_iter):
        atomMap = []
        for k,v in m.iteritems():
            atomMap.append([k,v])
        try:
            rmsd = chm.AlignMol(mol,ref,0,0,atomMap)
        except:
            continue
        w = rdk.PDBWriter(str(i)+file_mol.replace('.mol2','.pdb'))
        w.write(mol)
        w.close()

        if conf_bestRmsd is None or rmsd<conf_bestRmsd:
            conf_bestRmsd = rmsd

    print conf_bestRmsd
    
def main(options):
    
    mol_f = options.prob_mol
    tmp_dir = options.tmp_dir
    ref_f = options.ref_mol
    if mol_f is not None:
     print best_rmsd_firstConf(mol_f,ref_f)
    else:
     print best_rmsd_tmp_conf(tmp_dir,ref_f)
  

if __name__=='__main__':
  usage= 'python rmsd.py --probe=<probe_mol2_file> --ref=<ref_mol2_file>\n[-d (one2many rmsd) directory of probes files]\n[-m (many2many rmsd) directory of references files]'
  desc='Calculate probe molecule rmsd relative to reference molecule'
  parser = OptionParser(usage=usage,description=desc)
  parser.add_option("-r","--ref",type="string",action="store", dest="ref_mol",help="reference mol2 file")  
  parser.add_option("-p","--probe" ,type="string",action="store",dest="prob_mol",help="probe mol2 file")
  parser.add_option("-d","--tmp_dir" ,type="string",action="store",dest="tmp_dir",help="directory of temp charge conformation as probe (c_*.mol2)")

  options, args = parser.parse_args()  # default reads from argv[1:]
  if not options.ref_mol and not options.tmp_dir:
   if not options.prob_mol:
    parser.error("rmsd.py takes no positional arguments\n" +
                 "  Use --help for more information")
  main(options)
