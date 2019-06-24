#!/usr/local/python-2.7.11-ucs2/bin/python

import os, string, sys

from openeye.oechem import *

def Rxn(file1, file2, smirks, aa):

    try:

        ifs1 = oemolistream()
        
        ifs1.open(file1)
        
        ifs2 = oemolistream()
        
        ifs2.open(file1)
        
        ofs = oemolostream()
        
        ofs.open(file2)

    except IndexError:

        print '\nUsage: react.py in1.ism in2.ism out.ism \'reaction smarts\' \n'
        return
        #raise SystemExit()




    libgen1 = OELibraryGen(smirks)

    libgen1.SetExplicitHydrogens(aa==True)

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
    return
