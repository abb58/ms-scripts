#!/usr/local/

#===================================================================
# Convert the QE output to XYZ file
# Author : Abhishek Bagusetty, abb58@pitt.edu
# Date : Aug 11, 2015
# University of Pittsburgh
# VASP output is in Angstorm and this converts QE output from Bohr
#
# Usage : 
# python conv_QE_xyz.py pwscf_QE_data_file
#
# Output : 
# XYZ coord file
# 
# Use this with CAUTION: Please check the number of atoms, count of
# every element and number of config according to your needs.
#===================================================================

import os
import sys
import time

fname=sys.argv[1]
file=open(fname)

outf='QE-coord'
timestr = time.strftime("%Y-%m-%d:%H%M%S")
outf=outf+timestr+'.xyz'

# Remove if teh coord already exists
if(os.path.isfile(outf)):
   os.remove(outf)
outputfile=open(outf,'a')
energies=[]

# Skip all the test lines
file.readline()
file.readline()
file.readline()
file.readline()
file.readline()
file.readline()
file.readline()


for i in range(15): # No of Configs 
    file.readline()
    print('Writing Image : {0} '.format(i+1))
    outputfile.write('  53'+"\n")
    energies.append(file.readline())               # energies
    outputfile.write(energies[i])

    count=0
    while count<53: # No of atoms
        line=file.readline()
        fields=line.split()

        if count<24: # No of C atoms
           outputfile.write('C    {0:12f}     {1:12f}    {2:12f}'.format(float(fields[0])/1.8897, float(fields[1])/1.8897, float(fields[2])/1.8897 )+"\n")
        elif count>23 and count<28: # No of O atoms
           outputfile.write('O    {0:14f}     {1:14f}    {2:14f}'.format(float(fields[0])/1.8897, float(fields[1])/1.8897, float(fields[2])/1.8897 )+"\n")
        else:        # No of H atoms 
           outputfile.write('H    {0:14f}     {1:14f}    {2:14f}'.format(float(fields[0])/1.8897, float(fields[1])/1.8897, float(fields[2])/1.8897 )+"\n")
        count+=1
