
import rdkit.Chem as rdk
import rdkit.Chem.AllChem as chm
import sys



def prop2neighbours(atom,tracker,core):
    for a in atom.GetNeighbors():
        if a.GetIdx() in tracker:
            continue
        if a.GetSymbol()=='H':
            tracker.add(a.GetIdx())
            core.add(a.GetIdx())
            continue
	else:
#	if a.GetSymbol()=='C' or a.GetSymbol()=='N':
#        if str(a.GetHybridization())=='SP2':
            tracker.add(a.GetIdx())
            core.add(a.GetIdx())
#            prop2neighbours(a)



def findCore(mol):

    tracker = set()
    core = set()

    for a in mol.GetAtoms():
        if a.GetSymbol()=='Si':
            tracker.add(a.GetIdx())
            core.add(a.GetIdx())
            for a_i in a.GetNeighbors():
                tracker.add(a_i.GetIdx())
                core.add(a_i.GetIdx())
                if a_i.GetSymbol()=='C' or a_i.GetSymbol()=='S': # assumption SiH3 - link to either C or S
                    prop2neighbours(a_i,tracker,core)

    atoms2remove = []
    for a in mol.GetAtoms():
        if a.GetIdx() not in core:
	    atoms2remove.append(a.GetIdx())
	
    atoms2remove.sort(reverse=True)

    em = rdk.EditableMol(mol)
    for i in atoms2remove:
        em.RemoveAtom(i)

    return em.GetMol(),core


def main():
	mol = rdk.MolFromMol2File(sys.argv[1],removeHs=False)
	c,core = findCore(mol)

#	w = rdk.PDBWriter('core.pdb')
#	w.write(c)
#	w.close()

#	for a in c.GetAtoms():
#	    print a.GetSymbol()


	# create conf

	import random

	w = rdk.PDBWriter('rdkit_conf.pdb')
	num_conf = int(sys.argv[2])
	seed_track = set()	

	output_mol = None

	for i in range(0,num_conf):
	    new_mol = rdk.Mol(mol)
	    seed = 0
	    while seed==0 or seed in seed_track:
	    	seed = random.randrange(0,32000)
	    seed_track.add(seed)
	    #print seed
	    chm.ConstrainedEmbed(new_mol,c,randomseed=seed)
	    conf = new_mol.GetConformer(0)
	    conf.SetId(i)
	    if output_mol is None:
		 output_mol = rdk.Mol(new_mol)
	    else:
		for j in core:
		    conf.SetAtomPosition(j,output_mol.GetConformer(0).GetAtomPosition(j))
		output_mol.AddConformer(conf)
	w.write(output_mol)
	w.close()

if __name__=='__main__':
	main()
