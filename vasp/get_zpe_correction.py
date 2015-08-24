#!/usr/bin/python

# Performs zero point energy correction on the configuration 
# that has already gone through the phase of vibrational frequency analysis calculation.

# OUTPUT : Plot of potential energy surface

import numpy as np
import os
import datetime
import sys

ZPE = 0.0
frequencies = []
N = 53

outcar=sys.argv[1]
f=open(outcar)

#os.remove("zpe_output.txt") if os.path.isfile("zpe_output.txt")
if(os.path.isfile("zpe-output.txt")):
    os.remove("zpe_output.txt")

file=open('zpe_output.txt','a')
file.write('Working dir : {0}'.format(os.getcwd())+"\n")
file.write('Time : {0}'.format(datetime.datetime.now())+"\n")
file.write('Mode  Freq(Thz)   Wavenumber(cm-1)'+"\n")
    

while True:
    line = f.readline()
    if line.startswith(' Eigenvectors and eigenvalues of the dynamical matrix'):
        break
        
f.readline()  # skip ------
f.readline()  # skip two blank lines
f.readline()
for i in range(3*N):
    # the next line contains the frequencies
    line = f.readline()
    fields = line.split()
    
    if 'f/i=' in line:  # imaginary frequency
        # frequency in wave-numbers (meV)
        frequencies.append(complex(float(fields[6]), 0j))
    else:
        file.write('{0}  {1:6f}  {2:6f}'. format(fields[0], float(fields[3]), float(fields[7]))+"\n")
        frequencies.append(float(fields[7]))
        # now skip 1 one line, a line for each atom, and a blank line
    for j in range(1 + N + 1):
        f.readline()  # skip the next few lines
        
f.close()

#print frequencies
h = 4.1356675e-15 #eV*s
c = 3.0e10        #cm/s
ZPE = np.sum([0.5*h*c*f for f in frequencies if isinstance(f,float)]) # for f in cm-1

#ZPE = np.sum([0.5*f for f in frequencies if isinstance(f,float)]) # for f in meV

print('The ZPE correction is {0:1.6f} eV'.format(ZPE))
file.write('The ZPE correction is {0:1.6f} eV'.format(ZPE)+"\n")
file.close()
