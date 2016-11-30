#!/usr/local/python-2.7.11-ucs2/bin/python
import os, string, sys
from openeye.oechem import *

def UniMolRxn(ifs, ofs, umr):
    for mol in ifs.GetOEGraphMols():
        if umr(mol):
            OEWriteMolecule(ofs, mol)


def main(argv=[__name__]):
    if not (3 <= len(argv) <= 4):
        OEThrow.Usage("%s SMIRKS <infile> [<outfile>]" % argv[0])

    qmol = OEQMol()
    if not OEParseSmirks(qmol, argv[1]):
        OEThrow.Fatal("Unable to parse SMIRKS: %s" % argv[1])

    umr = OEUniMolecularRxn()
    if not umr.Init(qmol):
        OEThrow.Fatal("Failed to initialize reaction with %s SMIRKS" % argv[1])

    ifs = oemolistream()
    if not ifs.open(argv[2]):
        OEThrow.Fatal("Unable to open %s for reading" % argv[2])

    ofs = oemolostream(".ism")
    if len(argv) == 4:
        if not ofs.open(argv[3]):
            OEThrow.Fatal("Unable to open %s for writing" % argv[3])

    UniMolRxn(ifs, ofs, umr)

if __name__ == "__main__":
    sys.exit(main(sys.argv))

