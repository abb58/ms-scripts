#!/usr/bin/env python
import math
import sys

if len(sys.argv) == 1:
    file_outcar = 'OUTCAR' # default OUTCAR
elif len(sys.argv) == 2:
    file_outcar = sys.argv[1]
else:
    raise ValueError('too many arguments')

try:
    filein = open(file_outcar, 'r')
except IOError:
    print('No such file: ' + file_outcar)
    raise

content = filein.readlines()
filein.close()
max_forces = []
n_atoms = 0
for i, line in enumerate(content):
    # get number of atoms
    if 'number of ions     NIONS' in line:
        n_atoms = int(line.split()[-1])
        print('number of atoms :', n_atoms)
    # get maximum force for each iteration
    if 'TOTAL-FORCE' in line:
        max_forces.append(max([math.fabs(float(y)) for x in content[i + 2: i + 2 + n_atoms] for y in x.split()[3:]]))

for i in max_forces:
    print(i)
