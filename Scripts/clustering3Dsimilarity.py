#!/usr/bin/env python
#############################################################################
# Copyright (C) 2003-2015 OpenEye Scientific Software, Inc.
#############################################################################
# Align two compounds based on the maximum common substructure
#############################################################################
import sys
import os
from openeye.oechem import *


def MCSAlign(refmol, fitmol):
    atomexpr = OEExprOpts_AtomicNumber | OEExprOpts_Aromaticity
    bondexpr = 0
    mcss = OEMCSSearch(OEMCSType_Exhaustive)
    mcss.Init(refmol, atomexpr, bondexpr)
    mcss.SetMCSFunc(OEMCSMaxBondsCompleteCycles())

    unique = True
    overlay = False
    rms = []
    OESuppressHydrogens(fitmol)
    OESuppressHydrogens(refmol)
    for match in mcss.Match(fitmol, unique):
        ref_size = len(list(refmol.GetAtoms()))
        fit_size = len(list(fitmol.GetAtoms()))
        rms.append(OERMSD(mcss.GetPattern(), fitmol, match, overlay))
    coverage = len(list(match.GetAtoms())) * 2.0 / (ref_size + fit_size)
    rmsd = min(rms)
    if coverage > 0.75 and rmsd < 2.5:
        return True
    else:
        return False

def main(argv=[__name__]):
    if len(argv) != 3:
        OEThrow.Usage("%s <poses_folder> <cluster_folder>" % argv[0])
    os.mkdir(argv[2])
    reflist = [argv[1] + '/' + line for line in os.listdir(argv[1])]
    clusters_rep = [reflist[0]]
    clusters = [[reflist[0]]]

    counter = 0
    for refitem in reflist[1:]:
        counter += 1
        print counter
        print refitem
        reffs = oemolistream()
        if not reffs.open(refitem):
            OEThrow.Fatal("Unable to open %s for reading" % refitem)
        if not OEIs3DFormat(reffs.GetFormat()):
            OEThrow.Fatal("Invalid input format: need 3D coordinates")
        refmol = OEGraphMol()
        if not OEReadMolecule(reffs, refmol):
            OEThrow.Fatal("Unable to read molecule in %s" % refitem)
        if not refmol.GetDimension() == 3:
            OEThrow.Fatal("%s doesn't have 3D coordinates" % refmol.GetTitle())
        for i, cls in enumerate(clusters_rep):
            in_cluster = False
            clsfs = oemolistream()
            if not clsfs.open(cls):
                OEThrow.Fatal("Unable to open %s for reading" % cls)
            if not OEIs3DFormat(clsfs.GetFormat()):
                OEThrow.Fatal("Invalid input format: need 3D coordinates")
            fitmol = OEGraphMol()
            if not OEReadMolecule(clsfs, fitmol):
                OEThrow.Fatal("Unable to read molecule in %s" % cls)
            if not fitmol.GetDimension() == 3:
                OEThrow.Warning("%s doesn't have 3D coordinates" % fitmol.GetTitle())
                continue
            if MCSAlign(refmol, fitmol):
                in_cluster = True
                clusters[i].append(refitem)
                break
        if not in_cluster:
            clusters_rep.append(refitem)
            clusters.append([refitem])

    print len(clusters_rep)
    print len(clusters)
    print clusters[0][:10]
    for i, cls in enumerate(clusters):
        with open(argv[2] + '/cluster' + str(i) + '.mol2', 'w') as outfile:
            for fname in cls:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
