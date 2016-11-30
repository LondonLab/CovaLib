#!/usr/local/python-2.7.11-ucs2/bin/python
import os, string, sys
from openeye.oechem import *

try:
    ifs = oemolistream()
    ifs.open(sys.argv[1])
    ofs_1 = oemolostream()
    ofs_1.open(sys.argv[2])

except IndexError:
    print '\nUsage: react.py in.ism out.ism \'reaction smarts\' \n'
    raise SystemExit()

mol_si = OEGraphMol()
OEParseSmiles(mol_si, "[SiH3]")
libgen1 = OELibraryGen(sys.argv[3])
libgen1.SetExplicitHydrogens(False)
libgen1.SetValenceCorrection(True)

for mol in ifs.GetOEMols():
    libgen1.AddStartingMaterial(mol_si, 0)
    libgen1.AddStartingMaterial(mol, 1, False)
    mol.Clear()
    mol_si.Clear()

#uniqprod = []
for products in libgen1.GetProducts():
    smiles= OECreateSmiString(products)
    title=products.GetTitle()
    title=title[1:]
    products.SetTitle(title)
 #   if smiles not in uniqprod:
 #       uniqprod.append(smiles)
    OEWriteMolecule(ofs_1, products)

ofs_1.close()
ifs.close()
