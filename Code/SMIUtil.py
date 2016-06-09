from openeye.oechem import *
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
