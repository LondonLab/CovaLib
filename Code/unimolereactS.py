#!/usr/local/python-2.7.11-ucs2/bin/python

import os, string, sys

from openeye.oechem import *



def UniMolRxn(ifs, ofs, umr):

    for mol in ifs.GetOEGraphMols():

        if umr(mol):

            OEWriteMolecule(ofs, mol)
    return

def Parameters(name, file1, file2, smirks):

    print smirks
    argv = [name, file1, file2, smirks]
    main(argv)

def main(argv):

    if not (3 <= len(argv) <= 4):

        OEThrow.Usage("%s SMIRKS <infile> [<outfile>]" % argv[0] )



    qmol = OEQMol()

    if not OEParseSmirks(qmol, argv[3]):

        OEThrow.Fatal("Unable to parse SMIRKS: %s" % argv[3])



    umr = OEUniMolecularRxn()

    if not umr.Init(qmol):

        OEThrow.Fatal("Failed to initialize reaction with %s SMIRKS" % argv[3])



    ifs = oemolistream()

    if not ifs.open(argv[1]):

        OEThrow.Fatal("Unable to open %s for reading" % argv[1])



    ofs = oemolostream(".ism")

    if len(argv) == 4:

        if not ofs.open(argv[2]):

            OEThrow.Fatal("Unable to open %s for writing" % argv[2])



    UniMolRxn(ifs, ofs, umr)



#if __name__ == "__main__":

#    sys.exit(main(sys.argv))

