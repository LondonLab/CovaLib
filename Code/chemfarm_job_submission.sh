#!/bin/bash
#PBS -N un_sub_l
#PBS -q medium
#PBS -l select=1:ncpus=1:mem=512mb
#PBS -j eo

echo `hostname`
date

cd $PBS_O_WORKDIR
MYCOMMAND=/work/londonlab/git_dock/DOCK/docking/DOCK/src/i386/dock64
$MYCOMMAND
cd -

date
