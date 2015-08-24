#!/usr/bin/env python
# Code to read an CP2K MD unwrapped trajectory file and convert it to a wrapped xyz file
#
# Lx, Ly, Lz are the box dimensions
# xy,xz,yz are the tilt factors computed as follows

import numpy as np
from scipy import linalg as la
import argparse
import sys
import os

filename=sys.argv[1]
Lx=float(sys.argv[2])
Ly=float(sys.argv[3])
Lz=float(sys.argv[4])

if(os.path.isfile('coordwrapped.xyz')):
    os.remove('coordwrapped.xyz')

unwrapxyz = open(filename, 'r')
outputwrappedxyz = open('coordwrapped.xyz','a')
elements=[]

if len(sys.argv)!=5:
    print('Oops! Incorrect Arguments - '.format(len(sys.argv)))
else:
    # Compute the tilt factors
    lattice=[
        [9.8559999999999999,    0.0000000000000000,    0.0000000000000000],
        [-3.6959999999999997,    6.4016597847745800,    0.0000000000000000],
        [0.0000000000000000,    0.0000000000000000,   20.0000000000000000],
    ]
    a2x=np.divide(np.dot(lattice[0],lattice[1]),la.norm(lattice[0]))
    xy=np.divide(a2x,Ly)
    a3x=np.divide(np.dot(lattice[0],lattice[2]),la.norm(lattice[0]))
    xz=np.divide(a3x,Lz)
    yz=np.divide((np.dot(lattice[1],lattice[2])-np.multiply(a2x,a3x)) ,np.multiply(Lx,Lz))

    Natoms_string=unwrapxyz.readline() # No of atoms
    info=unwrapxyz.readline()   # Info on the step
    lines=unwrapxyz.readlines()
    print(len(lines))
    # Write the coordinates
    for i in range(len(lines)):
        if Natoms_string==lines[i]:
            natoms=int(lines[i])
            time_info=lines[i+1]
            outputwrappedxyz.write('{0}'.format(natoms)+"\n")
            outputwrappedxyz.write('{0}'.format(time_info))

            for j in range(natoms):
                data=lines[int(i+2+j)]
                fields=data.split()

                # Read the current time step
                elements.append(fields[0])
                xunwrap=float(fields[1])
                yunwrap=float(fields[2])
                zunwrap=float(fields[3])

                # Convert them to the wrapped coordinates
                xwrap = xunwrap-(xy*Ly)-(xz*Lz)-Lx
                ywrap = yunwrap-(yz*Lz)-Ly
                zwrap = zunwrap-Lz

                # Write the wrapped coordinates to a new xyz file
                outputwrappedxyz.write('{0} {1} {2} {3}'.format(elements[j],xwrap,ywrap,zwrap)+"\n")


unwrapxyz.close()
outputwrappedxyz.close()
