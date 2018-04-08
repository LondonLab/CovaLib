from rmsd import *
from optparse import OptionParser

def main(options):
 align(options.prob_mol,options.ref_mol,options.output_file)

if __name__=='__main__':
  usage= 'python align.py --probe=<probe_mol2_file> --ref=<ref_mol2_file> --output_file=<outputfile>'
  desc='Align probe molecule to Ref coordinates'
  parser = OptionParser(usage=usage,description=desc)
  parser.add_option("-r","--ref",type="string",action="store", dest="ref_mol",help="reference mol2 file")  
  parser.add_option("-i","--probe" ,type="string",action="store",dest="prob_mol",help="probe mol2 file")
  parser.add_option("-o","--output_file",type="string",action="store",dest="output_file",help="probe alignment output file")

  options, args = parser.parse_args()  # default reads from argv[1:]
  if 0 != len(args) or not options.ref_mol or not options.prob_mol:
    parser.error("align.py takes no positional arguments\n" +
                 "  Use --help for more information")
  main(options)

