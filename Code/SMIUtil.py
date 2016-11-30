from openeye.oechem import *
from openeye.oegraphsim import *
import sys
 

    
def get_canonical_smiles(smilein):
    """
    Converts the given smiles into a canonical SMILES string. assu
    Canonical SMILES - representing a given molecule, but without isotopic labeling or stereochemistry
    inpot - smiles string 
    output - the canonical form
    """      
    mol = OEGraphMol()
    if (OEParseSmiles(mol, smilein) == 1):
        smi = OECreateCanSmiString(mol)
        return "%s\n" % smi
    else:
        sys.stderr.write("%s is an invalid SMILES!" % smilein)

def tanimoto(smi1, smi2, i):
    if i == 0:
        FP = OEFPType_Lingo
    elif i == 1:
        FP = OEFPType_Path
    elif i == 2:
        FP = OEFPType_MACCS166
    molA = OEGraphMol()
    OESmilesToMol(molA, smi1)
    fpA = OEFingerPrint()
    OEMakeFP(fpA, molA, FP)

    molB = OEGraphMol()
    OESmilesToMol(molB, smi2)
    fpB = OEFingerPrint()
    OEMakeFP(fpB, molB, FP)

    return OETanimoto(fpA, fpB)
