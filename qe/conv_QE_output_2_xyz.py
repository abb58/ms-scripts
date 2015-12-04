#!usr/bin/python

# Performs single point calculations using Quantum espresso 
# each index from the trajectory file (.xyz). 
# Directories are created for each index. 
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
fxyz=open(file,'r')

for i in range(1,16):
    fxyz.readline() # No of atoms in XYZ file
    fxyz.readline() # Blank space / comments in XYZ 

    # Remove and create directories for each image
    if(os.path.exists('image_{0}'.format(i))):
        shutil.rmtree('image_{0}'.format(i), ignore_errors=True)
    os.mkdir('image_{0}'.format(i))
    os.chdir('image_{0}'.format(i))

    # Create input file
    f=open('spec_{0}.in'.format(i),'a')
    f.write('&CONTROL'+"\n")
    f.write('  calculation  = \'scf\',   ! single point calculation (default)'+"\n")
    f.write('  verbosity    = \'low\','+"\n")
    f.write('  nstep        = 1,'+"\n")
    f.write('  restart_mode = \'from_scratch\','+"\n")
    f.write('  pseudo_dir   = \'/mnt/mobydisk/gscratch1/kjohnson/abb58/pkg/espresso-5.2.0/pseudo/upf_files/\','+"\n")
    f.write('  outdir       = \'./\','+"\n")
    f.write('  prefix       = \'SPEC-I{0}\','.format(i)+"\n")
    f.write('  tprnfor      = .true.,'+"\n")
    f.write('  etot_conv_thr= 1.0D-11,'+"\n")
    f.write('  forc_conv_thr= 1.0D-9,'+"\n")
    f.write('/'+"\n")

    f.write('&SYSTEM'+"\n")
    f.write('  ibrav       = 0,          ! Lattice parameters are defined in the cell parameter '+"\n")
    f.write('  tot_charge  = +1,         ! total chg on the system'+"\n")
    f.write('  nat         = 53,'+"\n")
    f.write('  ntyp        = 3,'+"\n")
    f.write('  ecutwfc     = 50.D0,       ! kinetic energy cutoff (Ry) for wavefunctions'+"\n")
    f.write('  ecutrho     = 450.D0,      ! kinetic energy cutoff (Ry) for charge density'+"\n")
    f.write('/'+"\n")
    
    f.write('&ELECTRONS'+"\n")
    f.write('  conv_thr    = 1.0D-12,    ! convergence threashold on total energy'+"\n")
    f.write('/'+"\n")

    f.write('&IONS'+"\n")
    f.write('/'+"\n")

    f.write('ATOMIC_SPECIES'+"\n")
    f.write('C 12.0107 C.pbe-rrkjus.UPF'+"\n")
    f.write('O 15.9994 O.pbe-rrkjus.UPF'+"\n")
    f.write('H 1.00794 H.pbe-rrkjus.UPF'+"\n")

    f.write('ATOMIC_POSITIONS {angstrom}'+"\n")
    # Read and print the atomic coordinates from NEB trajectory
    count = 0
    while(count < 53):
        f.write(fxyz.readline())
        count += 1
                
    f.write('K_POINTS {automatic}'+"\n")
    f.write('3 3 1 0 0 0'+"\n")

    f.write('CELL_PARAMETERS {angstrom}'+"\n")
    f.write('9.8559999999999999    0.0000000000000000    0.0000000000000000'+"\n")
    f.write('-3.6959999999999997    6.4016597847745800    0.0000000000000000'+"\n")
    f.write('0.0000000000000000    0.0000000000000000   20.0000000000000000'+"\n")
    f.close()


    # Job script
    f=open("job.pbs",'a')
    f.write('#!/bin/bash'+"\n")
    f.write('#PBS -N QE-SPEC-{0}'.format(i)+"\n")
    f.write('#PBS -r n'+"\n")
    f.write('#PBS -j oe'+"\n")
    f.write('#PBS -M abb58@pitt.edu'+"\n")
    f.write('#PBS -q ib'+"\n")
    f.write('#PBS -l walltime=01:00:00,nodes=1:ppn=8'+"\n\n")

    f.write('INP=spec_{0}.in'.format(i)+"\n")
    f.write('OUT=SPEC-IMAGE_{0}.out'.format(i)+"\n")
    f.write('EXE=/mnt/mobydisk/gscratch1/kjohnson/abb58/pkg/espresso-5.2.0/bin/pw.x'+"\n\n")

    f.write('cd $PBS_O_WORKDIR'+"\n")
    f.write('module purge'+"\n")
    f.write('module load gcc/4.8.2-rhel'+"\n")
    f.write('module load intel/2015.1.133'+"\n")
    f.write('module load openmpi/1.8.4-intel15'+"\n")
    f.write('module load mkl/2015.1.133/icc-st-openmpi'+"\n")
    f.write('module load fftw/3.3.4-intel15'+"\n\n")

    f.write('prun --bind-to core $EXE -inp $INP > $OUT'+"\n")
    f.write('exit 0')
    f.close()

    #subprocess.call(["qsub job.pbs"])
    os.system("qsub job.pbs")

    # Change back the directory
    os.chdir('../')
