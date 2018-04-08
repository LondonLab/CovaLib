import mol2amsol as m2a
import sys

mol_list=m2a.read_Mol2_file(sys.argv[1])
ref = (m2a.read_Mol2_file(sys.argv[2]))[0]
for i,a in enumerate(mol_list[0].atom_list):
 a.Q = ref.atom_list[i].Q
m2a.write_mol2(mol_list[0],'c_'+sys.argv[1])

