#!/usr/bin/env python
#############################################################################
#  Copyright (C) 2003-2015 OpenEye Scientific Software, Inc.
#############################################################################
# Performing RMSD calculation between a 3D reference molecule and
# multi-conformation molecules
#############################################################################
import subprocess
import sys
import os
sys.path.append(os.path.dirname(sys.argv[0]) + "/../")
from Code import *
from openeye.oechem import *

def MCSAlign(refmol, fitmol, ofs):
    atomexpr = OEExprOpts_AtomicNumber | OEExprOpts_Aromaticity
    bondexpr = 0
    mcss = OEMCSSearch(OEMCSType_Exhaustive)
    mcss.Init(refmol, atomexpr, bondexpr)
    mcss.SetMCSFunc(OEMCSMaxBondsCompleteCycles())

    rmat = OEDoubleArray(9)
    trans = OEDoubleArray(3)
    unique = True
    overlay = True
    IDlist = []
    for match in mcss.Match(fitmol, unique):
        for ma,atm in zip(match.GetAtoms(), refmol.GetAtoms()):
            ID = ma.pattern.GetIdx()
            #print str(ID) + ' ' + atm.GetName()

       # print("target atoms:")
        for ma,atm in zip(match.GetAtoms(), fitmol.GetAtoms()):
            #print str(ma.target.GetIdx()) + ' ' + atm.GetName()
            IDlist.append(ma.target.GetIdx())

        #OEWriteMolecule(ofs, fitmol)
        return IDlist

def main(name, argv):
    if not len(argv) == 3:
        print_usage(name)
        return

    mparams = Mol2Utils.Mol2Utils(argv[0])
    mparams.process()
    mparams2 = Mol2Utils.Mol2Utils(argv[1])
    mparams2.process()
    new_atom_names = mparams2.get_atom_names()
    orig_atom_names = mparams.get_atom_names()

#    print new_atom_names

    fitfs = oemolistream()
    fitfs.open(argv[0])

    fitfs2 = oemolistream()
    fitfs2.open(argv[1])

    ofs = oemolostream()
    ofs.open(argv[2])
    for refmol in fitfs.GetOEGraphMols():
        for fitmol in fitfs2.GetOEGraphMols():
            map_list = MCSAlign(refmol, fitmol, ofs)
            for atom_num,orig_name in zip(map_list, orig_atom_names):
                new_atom_names[atom_num] = orig_name

#    print new_atom_names
    new_atom_names = new_atom_names[:len(map_list)]
    mparams2.switch_names(new_atom_names)
    mparams2.set_intro(mparams.get_intro())
    mparams2.set_bond(mparams.get_bond())
    mparams2.write_to_file(argv[2])
    mparams.close()
    mparams2.close()

def print_usage(name):
        print "Usage : " + name + " <ref mol> <fit mol(s)> <out mol(s)>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
