import rdkit.Chem as rdk
import rdkit.Chem.AllChem as chm
import rdkit.Geometry.rdGeometry as gt
from optparse import OptionParser
import math 
import networkx as nx
import networkx.algorithms.isomorphism as iso

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

def main(options):
    
    mol_f = options.prob_mol
    ref_f = options.ref_mol

    print best_rmsd_firstConf(mol_f,ref_f)
  

if __name__=='__main__':
  usage= 'python rmsd.py --probe=<probe_mol2_file> --ref=<ref_mol2_file>\n[-d (one2many rmsd) directory of probes files]\n[-m (many2many rmsd) directory of references files]'
  desc='Calculate probe molecule rmsd relative to reference molecule'
  parser = OptionParser(usage=usage,description=desc)
  parser.add_option("-r","--ref",type="string",action="store", dest="ref_mol",help="reference mol2 file")  
  parser.add_option("-p","--probe" ,type="string",action="store",dest="prob_mol",help="probe mol2 file")

  options, args = parser.parse_args()  # default reads from argv[1:]
  if 0 != len(args) or not options.ref_mol or not options.prob_mol:
    parser.error("rmsd.py takes no positional arguments\n" +
                 "  Use --help for more information")
  main(options)
