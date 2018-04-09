import rdkit.Chem as rdk
import rdkit.Chem.AllChem as chm
from optparse import OptionParser
import math 

def rmsdFirstConf(file_name_in,file_name_ref):
    in_mol = rdk.MolFromMol2File(file_name_in,removeHs=False)
    ref = rdk.MolFromMol2File(file_name_ref,removeHs=False)
    rmsd = getRmsdImmobile(in_mol,ref)
    #o3a_alignment = chm.GetO3A(in_mol,ref)
    #rmsd = o3a_alignment.Align()
    #rmsd = chm.GetBestRMS(in_mol,ref,0,0)
    return file_name_in,rmsd

def rmsdAllConf(file_name_in,file_name_ref):
    rmsd_arr = []
    in_mol = rdk.MolFromPDBFile(file_name_in)
    ref = rdk.MolFromPDBFile(file_name_ref)
    for i,conf in enumerate(in_mol.GetConformers()):
        rmsd_arr.append(chm.GetBestRMS(in_mol,ref,i,0))
    return rmsd_arr


def getRmsdImmobile(prbMol, refMol,
  prbConfId = -1, refConfId = -1, atomMap = None):
  refConf = refMol.GetConformer(refConfId)
  prbConf = prbMol.GetConformer(prbConfId)
  if (not atomMap):
    atomMap = []
    for i in range(0, refMol.GetNumAtoms()):
      if (refMol.GetAtomWithIdx(i).GetAtomicNum() == 1):
        continue
      atomMap.append((i, i))
  sqDist = 0.0
  for pair in atomMap:
    sqDist += (prbConf.GetAtomPosition(pair[0]) \
      - refConf.GetAtomPosition(pair[1])).LengthSq()
  sqDist /= float(len(atomMap))
  return math.sqrt(sqDist)

def main(options):

    file = options.prob_mol
    ref = options.ref_mol
    #print file,ref
    #print rmsdAllConf(file,ref)
    print rmsdFirstConf(file,ref)
  

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
