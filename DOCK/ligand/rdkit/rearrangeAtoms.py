from rmsd import *

def getFirstMatchByRef(mol,ref,iter):

    for m in iter:
        #print m
        dic_by_ref = {}
        for k,v in m.iteritems():
            #print mol.GetAtomWithIdx(k).GetSymbol(),ref.GetAtomWithIdx(v).GetSymbol()
            if mol.GetAtomWithIdx(k).GetSymbol()!=ref.GetAtomWithIdx(v).GetSymbol():
                break
            dic_by_ref[v] = k
        if len(dic_by_ref)!=len(ref.GetAtoms()): 
            continue
        #print m
        #print dic_by_ref
        return dic_by_ref
      
def getFirstMatch(mol,ref,iter):

    for m in iter:
        atom_count = 0
        for k,v in m.iteritems():
            if mol.GetAtomWithIdx(k).GetSymbol()!=ref.GetAtomWithIdx(v).GetSymbol():
                break
            atom_count+=1
        if atom_count!=len(ref.GetAtoms()):
            continue
        return m

def main(options):
    
    mol_f = options.probe_mol
    ref_f = options.ref_mol
    #out_f = options.out_file
    
    mol = rdk.MolFromMol2File(mol_f)
    ref = rdk.MolFromMol2File(ref_f)
    
    iter = getGraphIsoIter(mol,ref)
    m = getFirstMatchByRef(mol,ref,iter)
    for a in ref.GetAtoms():
       ref.GetConformer(0).SetAtomPosition(a.GetIdx(),mol.GetConformer(0).GetAtomPosition(m[a.GetIdx()]))
    w = rdk.PDBWriter('rearrange_'+mol_f.replace('.mol2','.pdb'))
    w.write(ref)
    w.close()
    

if __name__=='__main__':
  usage= 'python rearrangeAtoms.py --probe=<probe_mol2_file> --ref=<ref_mol2_file>'
  desc='Rearrange molecule atoms relative to reference molecule'
  parser = OptionParser(usage=usage,description=desc)
  parser.add_option("-r","--ref",type="string",action="store", dest="ref_mol",help="reference mol2 file")  
  parser.add_option("-p","--probe" ,type="string",action="store",dest="probe_mol",help="probe mol2 file")
  #parser.add_option("-o","--out_file" ,type="string",action="store",dest="out_file",help="the rearrange molecule output file name")


  options, args = parser.parse_args()  # default reads from argv[1:]
  if not options.ref_mol or not options.probe_mol:
    parser.error("rearrangeAtoms.py takes no positional arguments\n" +
                 "  Use --help for more information")
  main(options)

