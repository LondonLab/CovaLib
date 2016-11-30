import os
import PyUtils
import subprocess
import sys
import __main__
__main__.pymol_argv = ['pymol','-qc']
import pymol
from pymol import cmd, stored

def get_surface_area(file_name):    
    pymol.finish_launching()
    cmd.load(file_name)
    area = cmd.get_area('resi 1')
    cmd.remove(file_name[:-5])
    return area

def pymol_mutate(file_name, chain, res_index, number):
    pymol.finish_launching()
    cmd.delete(file_name[:-4])
    selection = chain + '/' + res_index + '/'
    mutant = 'CYS'
    cmd.wizard("mutagenesis")
    pdb = file_name[:-4]
    cmd.load(file_name)
    cmd.refresh_wizard()
    cmd.get_wizard().set_mode(mutant)
    cmd.get_wizard().do_select(selection)
    nStates = cmd.count_states("mutation")

    for i in range(1, nStates + 1):
        cmd.get_wizard().do_select(selection)
        cmd.frame(i)
        cmd.get_wizard().apply()
        cmd.save("rec_" + str(res_index) + "_" + str(i) + ".pdb")

    cmd.set_wizard()
    cmd.remove(file_name[:-4])

def show_bumps(selection):
    print selection
    name = 'bump_check'
    cmd.delete(name)
    cmd.create(name, selection, zoom=0)
    cmd.set('sculpt_vdw_vis_mode', 1, name)
    cmd.set('sculpt_field_mask', 0x020)  # cSculptVDW
    for state in range(1, 1 + cmd.count_states('%' + name)):
        cmd.sculpt_activate(name, state)
        strain = cmd.sculpt_iterate(name, state, cycles=0)
        print('VDW Strain in state %d: %f' % (state, strain))
