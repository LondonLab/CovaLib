#!/usr/arch/bin/python
"""Compute AM1BCC partial charges summing hydrogens into heavy atoms.

Michael Mysinger 200910 Created
"""

import sys
import logging
from optparse import OptionParser
from openeye.oechem import *
from openeye.oequacpac import *

def am1bcc(infile=None, outfile=None, hydrogens=False):
    if infile is None:
        ifs = oemolistream(".mol2")
    else:
        ifs = oemolistream(infile)
    if outfile is None:
        ofs = oemolostream(".mol2")
    else:
        if not (outfile.endswith(".mol2") or outfile.endswith(".mol2.gz")):
            logging.error("Output file must be .mol2 or .mol2.gz")
            return 2
        ofs = oemolostream(outfile)
    for mol in ifs.GetOEMols():
        OEAssignPartialCharges(mol, OECharges_AM1BCCSPt)
        if not hydrogens:
            counts = []
            for atom in mol.GetAtoms():
                count = 0
                if not atom.IsHydrogen():
                    for partner in atom.GetAtoms(OEIsHydrogen()):
                        atom.SetPartialCharge(atom.GetPartialCharge() +
                                       partner.GetPartialCharge())
                        partner.SetPartialCharge(0.0)
                        count += 1
                counts.append(count)
            OESetComment(mol, "United Counts: " +
                                  " ".join(str(x) for x in counts))
        OEFindRingAtomsAndBonds(mol)
        OEAssignAromaticFlags(mol, OEAroModelTripos)
        OETriposAtomTypes(mol)
        OETriposTypeNames(mol)
        OETriposBondTypeNames(mol)
        OEWriteMol2File(ofs, mol)
    return 0

def main(argv):
    """Parse arguments."""
    logging.basicConfig(level=logging.INFO, 
                        format='%(levelname)s: %(message)s')
    description = "Compute AM1BCC partial charges summing hydrogens into heavy atoms."
    usage = "%prog [options]"
    version = "%prog: version 200910 - created by Michael Mysinger"
    parser = OptionParser(usage=usage, description=description,
                          version=version)
    parser.set_defaults(infile=None, outfile=None, hydrogens=False)
    parser.add_option("-i", "--infile", 
                      help="input file (default: stdin)")
    parser.add_option("-o", "--outfile", 
                      help="output file (default: stdout)")
    parser.add_option("-k", "--keep-hydrogens", dest="hydrogens",
                      action="store_true",
                      help="keep hydrogen atoms")
    options, args = parser.parse_args(args=argv[1:])
    if len(args):
        parser.error("program takes no positional arguments.\n" +
                     "  Use --help for more information.")
    return am1bcc(infile=options.infile, outfile=options.outfile,
                  hydrogens=options.hydrogens)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
