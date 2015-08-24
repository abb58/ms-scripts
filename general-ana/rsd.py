#!/usr/bin/python

# Script to calculate the RSD as the reaction coordinate for NEB
# calculations.
# 
# RSD = \sqrt{\frac{1}{natoms} \sum{(v-w)^2 + (v-w)^2 +(v-w)^2}}
# Input : .xyz format trajectory of converged NEB replicas
# Output : Array of RSD distances for each snapshot referenced to first one
#
# Using it on Frank : 
# module load python/epd-7.2
# module load ase
#
# Abhishek Bagusetty (abb58@pitt.edu)
# University of Pittsburgh
# Aug 13,2015
#

import ase
import ase.io
import sys
import numpy as np

filename=sys.argv[1]
Nconfig=15
rmsd,rsd=[],[]
atoms_ref=ase.io.read(filename,index=0,format='xyz')
ref_positions=atoms_ref.get_positions()
natoms=atoms_ref.get_number_of_atoms()
inv_natoms=1.0/float(natoms)
rsd.append(0.0)
rmsd.append(0.0)

for i in range(1,Nconfig):
    temp=[]
    dist=0.0
    atoms=ase.io.read(filename,index=i,format='xyz')
    positions=atoms.get_positions()
    for j in range(natoms):
        temp.append( (ref_positions[j][0]-positions[j][0])**2 + 
                     (ref_positions[j][1]-positions[j][1])**2 + 
                     (ref_positions[j][2]-positions[j][2])**2 )
    dist=np.sum([k for k in temp])
    rsd.append( np.sqrt(dist) )
    rmsd.append( np.sqrt(inv_natoms * dist) )
print('Reaction Coordinate(RSD) array :{0}'.format(rsd)+"\n\n" )
print('Reaction Coordinate(RMSD) array :{0}'.format(rmsd) )
