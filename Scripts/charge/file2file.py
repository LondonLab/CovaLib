#!/usr/arch/bin/python
"""

Johannes Hermann 200602 Created
Michael Mysinger 200708 Modified for eel charges and optparse
Michael Mysinger 200804 Detect implicitH errors and keep old atom names 
Michael Mysinger 200810 Add ability to write to .eel1 files, including 
                          the ability to compute the new solvation column.
"""

import os
import sys
import gzip
import tempfile
from optparse import OptionParser
from openeye.oechem import *
#import mmmutils

VDW_SPECIFIC_TYPES = [("C.3", 5), ("N.4", 9), ("N.3", 10), ("O.3", 12)]
VDW_GENERIC_TYPES  = [("C.", 1), ("N.", 8), ("O.", 11), ("H", 7), 
                      ("S.", 14), ("P.", 13), ("F", 15), ("Cl", 16), 
                      ("Br", 17), ("I", 18), ("Si", 24), ("Na", 19), 
                      ("K", 19), ("Ca", 21), ("Li", 20), ("Al", 20), 
                      ("Du", 25), ("LP", 25)]
VDW_DEFAULT_TYPE = 25

def read_solv(filename):
    print 'Im here'
    print filename
    """Parse .solv file for atomic charge and solvation contributions.""" 
    #splits = list(mmmutils.read_splits(filename))
    splits = os.path.split(filename)
    # store charge to check atom association between mol2 and solv
    solv = [(float(x[0]), float(x[1]), float(x[3])) for x in splits[1:]]
    # return format is [(charge1, pol_solv1, apol_solv1), ]
    return solv

def read_united_counts(inf):
    counts = None
    f = open(inf)
    for line in f:
        if line.startswith("@<TRIPOS>ATOM"):
            break
        elif line.startswith("United Counts:"):
            splits = line.split()
            counts = [int(x) for x in splits[2:]]
            break
    f.close()
    return counts

def vdw_type(sybyl_type_string, h_count):
    """Convert sybyl atom type to dock atom type (without polar H type)."""
    instr = sybyl_type_string.strip()
    for (match, type) in VDW_SPECIFIC_TYPES:
        if instr == match:
            vdw = type
            break
    else:
        for (match, type) in VDW_GENERIC_TYPES:
            if instr.startswith(match):
                vdw = type
                break
        else:
            print ( "WARNING: unknown type for %s, " % instr + 
                        "its vdw parameters were zeroed!" )
            vdw = VDW_DEFAULT_TYPE
    if vdw == 5 and h_count > 0:
        vdw = 5 - h_count
    return vdw

def adjust_solv(solv, pos_solv=True):
    """Calculate total solvation including positive solvation adjustments."""
    # Dock empirically adjusts polar solvation by shifting all positive 
    #   polar solvation on to the atoms with negative polar solvation
    possolv = sum(psolv for (charge, psolv, asolv) in solv if psolv > 0.0)
    negsolv = sum(psolv for (charge, psolv, asolv) in solv if psolv <= 0.0)
    fraction = 1 + possolv/negsolv
    adj_solv = []
    for (charge, psolv, asolv) in solv:
        # total solvation = apolar solvation + adjusted polar solvation
        if pos_solv:
            if psolv > 0.0:
                tsolv = asolv
            else:
                tsolv = asolv + psolv * fraction
        else:
            tsolv = asolv + psolv
        adj_solv.append((charge, tsolv))
    return adj_solv

def f2f(inf, outf, canonical=False, gasteiger=False, solv_file=None, 
          pos_solv=True):
    """Convert input file to output file using Openeye's OEChem."""
    tfhandle, tfname = tempfile.mkstemp(suffix='.pdb')
    os.close(tfhandle)
    # Check for special united atom handling in mol2 -> eel1 conversion
    united_counts = None
    if inf.endswith('.mol2') and outf.endswith('.eel1'):
        united_counts = read_united_counts(inf)
    ifs = oemolistream()
    # Special handling for eel1 input
    if ( inf.endswith('.eel1') or inf.endswith('.1') or 
         inf.endswith('.eel1.gz') or inf.endswith('.1.gz') ):
        if inf.endswith('.gz'):
            eel = gzip.GzipFile(inf, 'rb')
        else:
            eel = open(inf, 'rU')
        tmpf = open(tfname, 'w')
        for line in eel:
            if line.startswith('ATOM'):
                nline = line[:54] + line[63:69] + line[55:62] + line[70:]
            elif 'energy' in line:
                nline = line.replace('REMARK', 'COMPND   ')
            else: 
                nline = line
            tmpf.write(nline)
        tmpf.close()
        eel.close()
        inf = tfname
        flavor = ( OEIFlavor_Generic_Default | OEIFlavor_PDB_Default | 
                   OEIFlavor_PDB_CHARGE | OEIFlavor_PDB_TER )
        ifs.SetFlavor(OEFormat_PDB, flavor)
    ifs.open(inf)
    if inf.endswith('.nmol2'):
        print "         Assuming mol2 format for .nmol2 input."
        ifs.SetFormat(OEFormat_MOL2)
    # Special handling for eel1 output
    if outf.endswith('.eel1'):
        if solv_file is None:
            print "WARNING: Assuming zeroes for solvation column in eel1 file."
            print "         Use -s option to add true desolvation information."
        else:
            solv = read_solv(solv_file)
            adj_solv = adjust_solv(solv, pos_solv=pos_solv)
        ofs = oemolostream(tfname)
    else:
        ofs = oemolostream(outf)
    mol_props = []
    for mol in ifs.GetOEMols():
        if OEHasExplicitHydrogens(mol) and OEHasImplicitHydrogens(mol):
            for atom in mol.GetAtoms():
                atom.SetImplicitHCount(0)
            OEAssignFormalCharges(mol)
        #OEPerceiveChiral(mol)
        if gasteiger:
            OEGasteigerPartialCharges(mol)
        if outf.endswith('.eel1'):
            # tag each atom with its solvation
            if solv_file:
                for atom, (charge, tsolv) in zip(mol.GetAtoms(), adj_solv):
                    # use charge to detect mismatch
                    if abs(atom.GetPartialCharge() - charge) > 0.01:
                        raise ValueError("Error: mismatch in atomic order " +
                            "detected between mol2 and solv files.")
                    atom.SetRadius(tsolv)
            # tag each atom with its vdw type
            for i, atom in enumerate(mol.GetAtoms()):
                if atom.IsPolarHydrogen():
                    vdw = 6
                else:
                    if united_counts:
                        h_count = united_counts[i]
                    else:
                        h_count = 0
                    vdw = vdw_type(atom.GetType(), h_count)
                atom.SetIntType(vdw)
        if canonical:
            OECanonicalOrderAtoms(mol)
            OECanonicalOrderBonds(mol)
        if outf.endswith('.mol2'):
            OEFindRingAtomsAndBonds(mol)
            OEAssignAromaticFlags(mol, OEAroModelTripos)
            OETriposAtomTypes(mol)
            OETriposTypeNames(mol)
            OETriposBondTypeNames(mol)
            OEWriteMol2File(ofs, mol, False)
        elif outf.endswith('.eel1'):
            #Switched due to atom order issues
            OEWritePDBFile(ofs, mol, OEPDBOFlag_DEFAULT | OEPDBOFlag_TER)
            #OEWriteConstMolecule(ofs, mol)
            props = [(atom.GetName(), atom.GetPartialCharge(), atom.GetRadius(), atom.GetIntType()) for atom in mol.GetAtoms()]
            mol_props.append(props)
        else:
            OEWriteMolecule(ofs, mol)
    ifs.close()
    ofs.close()
    if outf.endswith('.eel1'):
        # convert temporary .pdb to .eel1 by adding solvation and vdw info
        tmpf = open(tfname, 'r')
        eel = open(outf, 'w')
        i = 0
        j = 0
        for line in tmpf:
            if line.startswith("TER"):
                if len(line) < 5:
                    i += 1
                    nline = line
                else:
                    nline = ""
            elif line.startswith("ATOM") or line.startswith("HETATM"):
                atom = mol_props[i][j][0]
                if len(atom) < 4 and atom[0].isalpha():
                    atomf = " %-3.3s" % atom
                else:
                    atomf = "%-4.4s" % atom                 
                nline = ( line[:12] + atomf + line[16:54] +
                          "%8.3f%8.2f%3d\n" % mol_props[i][j][1:] )
                j += 1
            elif line.startswith("CONECT"):
                nline = ""
            else: 
                nline = line
            eel.write(nline)
        tmpf.close()
        eel.close()
        if "DEBUG" in os.environ:
            import shutil
            shutil.copy(tfname, os.path.splitext(outf)[0] + '.temp.pdb')
    if os.path.exists(tfname):
        os.remove(tfname)

def main(argv):
    """Parse arguments."""
    description = "Convert file from one type to another, including conversion to and from DOCK .eel1 files."
    usage = "%prog [options] infile outfile"
    version = "%prog: version 200810 - created by Johannes Herman & Michael Mysinger"
    parser = OptionParser(usage=usage, description=description,
                          version=version)
    parser.set_defaults(canonical=False, gasteiger=False, solvation=None, 
                        pos_solv=True)
    parser.add_option("-c", "--canonical", action="store_true", 
           help="canonicalize atoms and bonds")  
    parser.add_option("-g", "--gasteiger", action="store_true", 
           help="generate gasteiger charges")
    parser.add_option("-s", "--solvation",
           help="solvation data (as output by RunAMSOL3.csh)")
    parser.add_option("-p", "--pos-solv", action="store_false", 
           help="disable positive solvation adjustment")
    options, args = parser.parse_args(args=argv[1:])
    if len(args) != 2:
        parser.error("program takes infile and outfile as arguments.\n" +
                     "  Use --help for more information.")
    f2f(args[0], args[1], canonical=options.canonical, 
          gasteiger=options.gasteiger, solv_file=options.solvation,
          pos_solv=options.pos_solv)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
