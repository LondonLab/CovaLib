import sys,os,math
import Bio.PDB

def main(name, argv):
    # correct this later!
        if (len(argv) <> 4):
                print_usage(name)
                return

    # Select what residues numbers you wish to align
    # and put them in a list
	start_id = int(argv[2])
   	end_id   = int(argv[3])
	atoms_to_be_aligned = range(start_id, end_id + 1)

    # Start the parser
	pdb_parser = Bio.PDB.PDBParser(QUIET = True)

    # Get the structures
	ref_structure = pdb_parser.get_structure("reference", 'PDB/'+argv[0])
	sample_structure = pdb_parser.get_structure("samle", 'PDB/'+argv[1])

    # Use the first model in the pdb-files for alignment
    # Change the number 0 if you want to align to another structure
	ref_model    = ref_structure[0]
	sample_model = sample_structure[0]

    # Make a list of the atoms (in the structures) you wish to align.
    # In this case we use CA atoms whose index is in the specified range
	ref_atoms = []
	sample_atoms = []
	ref_res_id = []
	sample_res_id = []

    # Iterate of all chains in the model in order to find all residues
	for ref_chain in ref_model:
      # Iterate of all residues in each model in order to find proper atoms
		for ref_res in ref_chain:
        # Check if residue number ( .get_id() ) is in the list
			if ref_res.get_id()[1] in atoms_to_be_aligned:
				ref_res_id.append(ref_res.get_id()[1])
          
    # Do the same for the sample structure
	for sample_chain in sample_model:
		for sample_res in sample_chain:
			if sample_res.get_id()[1] in atoms_to_be_aligned:
				sample_res_id.append(sample_res.get_id()[1])

   # Cross out elements that are not in both of lists: sample_atoms and ref_atoms
	i = 0; j = 0
	#print len(ref_res_id)
	#print len(sample_res_id)
	while (i < len(ref_res_id)) or (j < len(sample_res_id)):
		if ref_res_id[i] == sample_res_id[j]:
			i += 1
			j += 1
		elif ref_res_id[i] > sample_res_id[j]:
			del sample_res_id[j]
		else:
			del ref_res_id[i]

    # Iterate of all chains in the model in order to find all residues
	for ref_chain in ref_model:
      # Iterate of all residues in each model in order to find proper atoms
		for ref_res in ref_chain:
        # Check if residue number ( .get_id() ) is in the list
			if ref_res.get_id()[1] in ref_res_id:
          # Append CA atom to list
				ref_atoms.append(ref_res['CA'])

    # Do the same for the sample structure
	for sample_chain in sample_model:
		for sample_res in sample_chain:
			if sample_res.get_id()[1] in sample_res_id:
				sample_atoms.append(sample_res['CA'])

    # Now we initiate the superimposer:
	super_imposer = Bio.PDB.Superimposer()
	super_imposer.set_atoms(ref_atoms, sample_atoms)
	super_imposer.apply(sample_model.get_atoms())

    # Print RMSD:
	print super_imposer.rms

    # Save the aligned version of reference.pdb
	io = Bio.PDB.PDBIO()
	io.set_structure(sample_structure) 
	io.save(argv[0]+"_aligned.pdb")
        
def print_usage(name):
	print "Usage : " + name + " <reference_molecule> <samle_molecule> <start_residue> <end_residue> "

if __name__ == "__main__":
        main(sys.argv[0], sys.argv[1:])
