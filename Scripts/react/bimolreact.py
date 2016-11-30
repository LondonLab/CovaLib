#!/usr/local/python-2.7.11-ucs2/bin/python
import os, string, sys
from openeye.oechem import *

try:
    ifs1 = oemolistream()
    ifs1.open(sys.argv[1])
    ifs2 = oemolistream()
    ifs2.open(sys.argv[2])
    ofs = oemolostream()
    ofs.open(sys.argv[3])

except IndexError:
    print '\nUsage: react.py in1.ism in2.ism out.ism \'reaction smarts\' \n'
    raise SystemExit()


libgen1 = OELibraryGen(sys.argv[4])
libgen1.SetExplicitHydrogens(False)
libgen1.SetValenceCorrection(True)

for mol1 in ifs1.GetOEMols():
  libgen1.AddStartingMaterial(mol1, 0)
for mol2 in ifs2.GetOEMols():  
    libgen1.AddStartingMaterial(mol2, 1)
#      mol2.Clear()
#  mol1.Clear()

#uniqprod = []
for products in libgen1.GetProducts():
    smiles= OECreateSmiString(products)
    title=products.GetTitle()
    #title=title[1:]
    products.SetTitle(title)
 #   if smiles not in uniqprod:
 #       uniqprod.append(smiles)
    OEWriteMolecule(ofs, products)

ofs.close()
ifs1.close()
ifs2.close()
