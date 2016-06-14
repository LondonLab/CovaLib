#!/usr/local/python-2.7.11-ucs2/bin/python
#############################################################################
#  Copyright (C) 2003-2015 OpenEye Scientific Software, Inc.
#############################################################################
# Performing RMSD calculation between a 3D reference molecule and
# multi-conformation molecules
#############################################################################
import sys
from openeye.oechem import *


def main(argv=[__name__]):
    rmsdout = "rmsd.txt"
    itf = OEInterface(InterfaceData, argv)

    if not itf.GetBool("-verbose"):
        OEThrow.SetLevel(OEErrorLevel_Warning)

    rfname = itf.GetString("-ref")
    ifname = itf.GetString("-in")
    
    automorph = itf.GetBool("-automorph")
    heavy = itf.GetBool("-heavyonly")
    overlay = itf.GetBool("-overlay")

    ifs = oemolistream()
    if not ifs.open(rfname):
        OEThrow.Fatal("Unable to open %s for reading" % rfname)

    rmol = OEGraphMol()
    if not OEReadMolecule(ifs, rmol):
        OEThrow.Fatal("Unable to read reference molecule")

    ifs = oemolistream()
    if not ifs.open(ifname):
        OEThrow.Fatal("Unable to open %s for reading" % ifname)

    ofs = oemolostream()
    if itf.HasString("-out"):
        ofname = itf.GetString("-out")
        if not ofs.open(ofname):
            OEThrow.Fatal("Unable to open %s for writing" % ofname)
        if not overlay:
            OEThrow.Warning("Output is the same as input when overlay is false")

    rmsdfile = open(rmsdout, 'w')
    min_rmsd_file = "min_rmsd.mol2"
    minfs = oemolostream()
    min_rmsd = 1000
    for mol in ifs.GetOEMols():
        OEThrow.Info(mol.GetTitle())

        rmsds = OEDoubleArray(mol.GetMaxConfIdx())
        rmtx = OEDoubleArray(9 * mol.GetMaxConfIdx())
        tmtx = OEDoubleArray(3 * mol.GetMaxConfIdx())

        # perform RMSD for all confomers
        OERMSD(rmol, mol, rmsds, automorph, heavy, overlay, rmtx, tmtx)
        rmsdfile.write(str(rmsds[0]) + '\n')

        for conf in mol.GetConfs():
            cidx = conf.GetIdx()
            OEThrow.Info("Conformer %i : rmsd = %f" % (cidx, rmsds[cidx]))

            if itf.GetBool("-overlay"):
                OERotate(conf, rmtx[cidx * 9: cidx * 9 + 9])
                OETranslate(conf, tmtx[cidx * 3: cidx * 3 + 3])

        if rmsds[0] < min_rmsd:
            min_rmsd = rmsds[0]
            minfs.open(min_rmsd_file)
            OEWriteMolecule(minfs, mol)

        if itf.HasString("-out"):
            OEWriteMolecule(ofs, mol)

    rmsdfile.close()
    return 0

#############################################################################

InterfaceData = """\
!BRIEF [options] [-ref <mol file>] [-in <mol file>] [-out <mol file>]

!CATEGORY "input/output options"

  !PARAMETER -ref
    !TYPE string
    !REQUIRED true
    !BRIEF input reference mol file name
    !KEYLESS 1
  !END

  !PARAMETER -in
    !ALIAS -i
    !TYPE string
    !REQUIRED true
    !BRIEF input mol file name
    !KEYLESS 2
  !END

  !PARAMETER -out
    !ALIAS -o
    !TYPE string
    !REQUIRED false
    !BRIEF output file name, this implies that -overlay should be true
    !KEYLESS 3
  !END

!END

!CATEGORY "options"

  !PARAMETER -automorph
    !TYPE bool
    !DEFAULT true
    !BRIEF assign best atom association
    !DETAIL
        If false, atoms are associated by order.
        If true, graph isomorphism is determined with symmetry perception.
  !END

  !PARAMETER -overlay
    !TYPE bool
    !DEFAULT true
    !BRIEF Minimize to the smallest RMSD
  !END

  !PARAMETER -heavyonly
    !TYPE bool
    !DEFAULT true
    !BRIEF Ignore hydrogens for RMSD calculation
  !END

  !PARAMETER -verbose
    !ALIAS -v
    !TYPE bool
    !DEFAULT false
    !BRIEF verbose
  !END

!END
"""

#############################################################################
if __name__ == "__main__":
    sys.exit(main(sys.argv))
