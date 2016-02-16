#!/usr/bin/python

import ase
import sys
import numpy as np
import ase.io

# Get the supercell as an input
filename=sys.argv[1]
atoms=ase.io.read(filename,index=0,format='xyz')


# Set the Lattice Parameters information & PBC info
cell = [(20.38145975, 0.0, 0.0),
        (-7.64304740, 13.237758, 0.0),
        (0, 0, 40.0)]
atoms.set_cell(cell, scale_atoms=False, fix=None)
atoms.set_pbc((True, True, True))
ase.io.write('origatoms.png', atoms, show_unit_cell=True)


# Replicate how many units in each direction
replicate=(2,2,1)
repeatatoms=atoms.repeat(replicate)


# Write out the replicated file in xyz format
ase.io.write('repeatatoms-{0}.png'.format(replicate), repeatatoms, rotation='-73x', show_unit_cell=True)
ase.io.write('replicated-{0}.xyz'.format(replicate), repeatatoms)


