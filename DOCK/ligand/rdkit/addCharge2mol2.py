import mol2amsol as m2a
import sys
from optparse import OptionParser

def main(options):
 
    mol_f = options.probe_mol
    ref_f = options.ref_mol
    out_f = options.out_file

    if not out_f:
	out_f = 'c_'+mol_f
    #print '---> output file:',out_f

    mol_list=m2a.read_Mol2_file(mol_f)
    ref = (m2a.read_Mol2_file(ref_f))[0]

    for i,a in enumerate(mol_list[0].atom_list):
        a.Q = ref.atom_list[i].Q
    
    m2a.write_mol2(mol_list[0],out_f)
    

if __name__=='__main__':
  usage= 'python addCharge2mol2.py --probe=<probe_mol2_file> --ref=<ref_mol2_file>'
  desc='Add charge to atoms based on reference molecule atoms (need to be isomorphic'
  parser = OptionParser(usage=usage,description=desc)
  parser.add_option("-r","--ref",type="string",action="store", dest="ref_mol",help="reference mol2 file")  
  parser.add_option("-p","--probe" ,type="string",action="store",dest="probe_mol",help="probe mol2 file")
  parser.add_option("-o","--out_file" ,type="string",action="store",dest="out_file",help="the chargerd molecule output file name")


  options, args = parser.parse_args()  # default reads from argv[1:]
  if not options.ref_mol or not options.probe_mol:
    parser.error("addCharge2mol2.py takes no positional arguments\n" +
                 "  Use --help for more information")

  main(options)
