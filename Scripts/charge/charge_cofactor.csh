#!/bin/csh

if ( $#argv < 2 || $#argv > 3 ) then
    echo
    echo "Generate prot.table and amb.crg with am1bcc charges."
    echo
    echo "usage: charge_cofactor.csh input.mol2 RES [hydrogens]"
    echo
    echo "input.mol2: all atom version of input molecule ionized properly"
    echo "RES: final three-letter residue code (upper case)"
    echo "optional hydrogens: flag to keep hydrogen atoms"
    echo
    echo "Note: SYBYL atom and bond types need to be correct in input mol2!"
    echo
    echo "Typical use pattern: "
    echo "1) Download ligand pdb from ligandexpo"
    echo "2) Manipulate pdb by removing atoms and their connect records"
    echo "       in text editor"
    echo "3) file2file.py blah.pdb blah.mol2"
    echo "       This preserves atom names"
    echo "4) Check mol2 sybyl atom types in chimera, label -> other -> mol2"
    echo
    exit 1
endif

if ( $1:e != 'mol2' ) then
    echo
    echo "Please create an all atom .mol2 to use as input."
    echo "Also be sure it looks right and has the correct ionization state."
    echo
    exit 1
endif

if ( $#argv > 2 ) then
    set hydrogens = "true"
else
    set hydrogens = "false"
endif

set base=$0:h
if ( "$base" == "$0" ) then
    set base="."
endif

if ( "$hydrogens" == "true" ) then
    python $base/am1bcc.py -k -i $1 -o $1:r_molcharge.mol2
else
    python $base/am1bcc.py -i $1 -o $1:r_molcharge.mol2
endif 

python $base/file2file.py $1:r_molcharge.mol2 $1:r_molcharge.eel1
$base/eel2prot.py -i $1:r_molcharge.eel1 -o $1:r_molcharge.prot.table
sed "s/UNL/$2/" $1:r_molcharge.prot.table >! $1:r.prot.table
$base/prot2crg.py -i $1:r.prot.table -o $1:r.amb.crg
rm -f $1:r_molcharge.mol2 $1:r_molcharge.eel1 $1:r_molcharge.prot.table

