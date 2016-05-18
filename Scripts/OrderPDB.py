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

def MCSAlign(refmol, fitmol):
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
        for ma,atm in zip(match.GetAtoms(), fitmol.GetAtoms()):
            IDlist.append(ma.target.GetIdx())
        return IDlist

def main(name, argv):
    if not len(argv) == 4:
        print_usage(name)
        return

    mparams = Mol2Utils.Mol2Utils(argv[0])
    mparams.process()
    mparams2 = Mol2Utils.Mol2Utils(argv[1])
    mparams2.process()
    new_atom_names = mparams2.get_atom_names()
    orig_atom_names = mparams.get_atom_names()

    fitfs = oemolistream()
    fitfs.open(argv[0])

    fitfs2 = oemolistream()
    fitfs2.open(argv[1])

    for refmol in fitfs.GetOEGraphMols():
        for fitmol in fitfs2.GetOEGraphMols():
            map_list = MCSAlign(refmol, fitmol)
            for atom_num,orig_name in zip(map_list, orig_atom_names):
                new_atom_names[atom_num] = orig_name

    map_num = len(map_list)
    new_atom_names = new_atom_names[:map_num]

    for i in range(1, int(argv[3]) + 1):
        f = open(argv[2] + "_%04d.pdb" % i, 'r')
        lines = f.readlines()
        f.close()
        lines = lines[:map_num] + [lines[-1]]
        f = open(argv[2] + '_%04d.pdb' % i , 'w')
        for atom, line in zip(new_atom_names, lines):
            line = line[:13] + atom[-3:] + ' ' + line[16:]
            f.write(line)
        f.write(lines[-1])
        f.close()

def print_usage(name):
        print "Usage : " + name + " <ref mol> <fit mol(s)> <PDB prefix> <number>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
