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
    if not len(argv) == 3:
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
            #for atom_num,orig_name in zip(map_list, orig_atom_names):
                #new_atom_names[atom_num] = orig_name
            break
    #print 'pdb: ' + argv[2]
    #print 'fit: ' + argv[1] + str(new_atom_names)
    #print 'ref:' + argv[0] + str(orig_atom_names)
    #print map_list
    map_num = len(map_list)
    new_atom_names = new_atom_names[:map_num]
    with open(argv[2], 'r') as fpdb:
        lines = fpdb.readlines()
    tmp_lines = []
    for line in lines:
        if line[0] == 'H':
            tmp_lines.append(line)
    lines = tmp_lines
    with open(argv[2], 'w') as fpdb:
        for line in lines:
            if line[0] == 'H':
                for i, item in enumerate(orig_atom_names):
                    if line[12:15] in item:
                        num = map_list[i]
                        break
                #print str(num) + ' ' + new_atom_names[num] + ' ' + line[12:15]
                fpdb.write(line[:12] + new_atom_names[num] + line[15:])
            if line[0] == 'T':
                fpdb.write(line)
    '''for i in range(1, int(argv[3]) + 1):
        f = open(argv[2] + "_%04d.pdb" % i, 'r')
        lines = f.readlines()
        f.close()
        lines = lines[:map_num] + [lines[-1]]
        f = open(argv[2] + '_%04d.pdb' % i , 'w')
        for atom, line in zip(new_atom_names, lines):
            line = line[:13] + atom[-3:] + ' ' + line[16:]
            f.write(line)
        f.write(lines[-1])
        f.close()'''

def print_usage(name):
        print "Usage : " + name + " <ref mol> <fit mol(s)> <pdb name>"

if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
