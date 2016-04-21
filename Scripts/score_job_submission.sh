#!/bin/bash
#PBS -N un_sub_l
#PBS -q medium
#PBS -l select=1:ncpus=1:mem=512mb
#PBS -j eo

echo `hostname`
date

cd $PBS_O_WORKDIR

module load python/2.7.11-ucs2
export PYTHONPATH=/work/londonlab/software/openeye/OpenEye-toolkits-python2.7-redhat-6-x64-2016.2.1
export OE_LICENSE=/work/londonlab/software/openeye/oe_license.txt


MYCOMMAND="python /home/dinad/CovaLib/Scripts/Ligand_score.py PDB_list.txt"
$MYCOMMAND

cd -

date
