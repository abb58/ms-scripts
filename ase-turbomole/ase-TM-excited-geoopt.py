#!/bin/bash/python

# Script written for Karl Johnson Group at University 
# of Pittsburgh
# Author : Abhishek Bagusetty
# Date   : July 25,2015

import os
from subprocess import Popen, PIPE, STDOUT

from ase import Atoms
from ase.calculators.turbomole import Turbomole
from ase.io import read,write

# Delete old coord, control, ... files, if exist
for f in ['coord',
          'basis',
          'energy',
          'mos',
          'statistics',
          'control'
          'job.*']:
    if os.path.exists(f):
        os.remove(f)

atoms = read('replica00.xyz')
atoms.set_calculator(Turbomole()) # Writes a coord file as well

# Write all commands for the define command in a string (GEO_OPT with DFT)
# Basis - def2-TZVP
# SCF conv 10e-8
# SCF iter 999
# Functional - b3-lyp
define_str = '\nexcite-geo-opt\na coord\n*\nno\nb all def2-TZVP\n*\neht\ny\n1\ny\nscf\nconv\n8\niter\n999\n\nex\nrpas\nq\na 1000\nq\nrpacor 1000\nq\ny\ndft\non\nfunc b3-lyp\n\n*'

# Run define
p = Popen('define', stdout=PIPE, stdin=PIPE, stderr=STDOUT)
stdout = p.communicate(input=define_str)

# Run turbomole for TDDFT
os.system('jobex -dscf -level=scf -energy 6 -c 1000 > jobex.out')
