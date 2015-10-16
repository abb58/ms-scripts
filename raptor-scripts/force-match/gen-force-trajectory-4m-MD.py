#!usr/bin/python

# Generates several configurations to compute forces for the 
# trajectory at various intervals from a MD trajectory.
# Please note the output is just a xyz trajectory which
# can be further used for force calculations.
#
# INPUT : AIMD trajectory
# usage : python gen-force-trajectory-4m-MD.py <FILENAME-inputMDtraj.xyz>
#
# Abhishek Bagusetty

import os
import shutil
import datetime
import sys
import numpy as np
import subprocess

# Read the coordinates from NEB path
file=sys.argv[1]

for i in range(1,4):
    print('---- RUN : {0} ----'.format(i))
    fxyz=open(file,'r')
    fref=open('FREF_{0}.xyz'.format(i),'a')

    count = 0
    if(i == 1):
        check = list(range(5000,105100,100))
    elif(i == 2):
        check = list(range(5130,105130,100))
    elif(i == 3):
        check = list(range(5160,105160,100))

    while(count<1000):
        line = fxyz.readline();
        if(line.startswith(' i = ')):
            fields = line.split();
            field = int(fields[2].rstrip(","))
            if( field == check[count] ):
                print('Writing Config : {0}'.format(count))
                fref.write('    61'+"\n")
                fref.write(' i = {0}'.format(count)+"\n")
                count = count+1
                for i in range(1,62):
                    coord = fxyz.readline()
                    fref.write(coord)

    fxyz.close()
    fref.close()
