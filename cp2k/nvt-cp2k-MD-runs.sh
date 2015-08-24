#!/bin/bash

runs="1 2 3 4 5"
temp="600 900"

# Command-line arguments !!
functional=$1
ensemble=$2
queue=$3

########### Specify the potentials ###########
if [ "$1" == "PBE" ]; then
    potential_H='GTH-PBE-q1';
    potential_C='GTH-PBE-q4';
    potential_O='GTH-PBE-q6';
elif [ "$1" == 'HCTH120' ]; then
    potential_H='GTH-HCTH120-q1';
    potential_C='GTH-HCTH120-q4';
    potential_O='GTH-HCTH120-q6';
elif [ "$1" == 'BLYP' ]; then
    potential_H='GTH-BLYP-q1';
    potential_C='GTH-BLYP-q4';
    potential_O='GTH-BLYP-q6';
else
    echo 'Potential NOT found for the this type !!!!. Quitting....'
    exit 1;
fi

for i in $runs; do
    mkdir -p run_$i
    cd run_$i
    for j in $temp; do
	mkdir -p ${j}k
	cd ${j}k
	echo "###########################################
############### Input file ################
###########################################
@SET CHARGE     1
@SET CUTOFF     440
@SET RELCUTOFF  40
@SET SCF_CONV   1.0E-8
@SET FUNCTIONAL $functional
@SET RUN_TYPE   MD
@SET ENSEMBLE_TYPE   $ensemble
@SET MAX_SCF    500
@SET PROJECT    $ensemble-${j}k-$functional
@SET POSITION_FILE ../../../relax-fullyOH.xyz

&GLOBAL
  PRINT_LEVEL LOW
  PROJECT_NAME \${PROJECT}
  RUN_TYPE \${RUN_TYPE}
  &MACHINE_ARCH
    PRINT_FULL TRUE
  &END MACHINE_ARCH
&END GLOBAL

&FORCE_EVAL
  METHOD QS
  &DFT
    BASIS_SET_FILE_NAME /home/kjohnson/abb58/cp2k-2.7/cp2k/data/BASIS_MOLOPT
    POTENTIAL_FILE_NAME /home/kjohnson/abb58/cp2k-2.7/cp2k/data/GTH_POTENTIALS
    CHARGE              \${CHARGE}

    &MGRID
      ! PW cutoff ... depends on the element (basis) too small cutoffs lead to the eggbox effect.
      ! certain calculations (e.g. geometry optimization, vibrational frequencies,
      ! NPT and cell optimizations, need higher cutoffs)
      NGRIDS     5
      CUTOFF     \${CUTOFF}
      REL_CUTOFF \${RELCUTOFF}
    &END MGRID

    &QS
       ! use the GPW method (i.e. pseudopotential based calculations with the Gaussian and Plane Waves scheme).
       METHOD GPW
       ! default threshold for numerics ~ roughly numerical accuracy of the total energy per electron,
       ! sets reasonable values for all other thresholds.
       EPS_DEFAULT 1.0E-10
       ! used for MD, the method used to generate the initial guess.
       EXTRAPOLATION ASPC
    &END QS

    &POISSON
       PERIODIC XYZ ! the default, gas phase systems should have 'NONE' and a wavelet solver
    &END

    &PRINT
       ! at the end of the SCF procedure generate cube files of the density
       &E_DENSITY_CUBE OFF
       &END E_DENSITY_CUBE
       ! compute eigenvalues and homo-lumo gap each 10nd MD step
       &MO_CUBES OFF
          NLUMO 4
          NHOMO 4
          WRITE_CUBE .FALSE.
          &EACH
            MD 1000
          &END
       &END
    &END

    &SCF
      SCF_GUESS RESTART
      EPS_SCF \${SCF_CONV}
      MAX_SCF \${MAX_SCF}

      &OT
        ! an accurate preconditioner suitable also for larger systems
        PRECONDITIONER FULL_KINETIC
        ! the most robust choice (DIIS might sometimes be faster, but not as stable).
        MINIMIZER DIIS
      &END OT

      &OUTER_SCF
        MAX_SCF 10
        EPS_SCF \${SCF_CONV}
      &END OUTER_SCF

      &PRINT
        &RESTART OFF
        &END
      &END
    &END SCF

    &XC
      &XC_FUNCTIONAL \${FUNCTIONAL}
      &END XC_FUNCTIONAL
    &END XC

    @IF (\${FUNCTIONAL} == 'BLYP')
      &VDW_POTENTIAL
        DISPERSION_FUNCTIONAL PAIR_POTENTIAL
        &PAIR_POTENTIAL
          TYPE DFTD3
          PARAMETER_FILE_NAME /opt/pkg/cp2k/2.6/dist/cp2k/data/dftd3.dat
          REFERENCE_FUNCTIONAL BLYP
          VERBOSE_OUTPUT TRUE
        &END PAIR_POTENTIAL
      &END VDW_POTENTIAL
    @ENDIF
  &END DFT

  &SUBSYS
    &CELL
      ABC              9.856  7.392   20.000
      ALPHA_BETA_GAMMA 90.000 90.000 120.000
      PERIODIC XYZ
    &END CELL
    &TOPOLOGY
      COORD_FILE_NAME \${POSITION_FILE}
      COORDINATE XYZ
    &END TOPOLOGY
    &KIND O  # OXYGEN ATOM
      BASIS_SET DZVP-MOLOPT-SR-GTH-q6
      POTENTIAL ${potential_O}
    &END KIND
    &KIND H  # HYDROGEN ATOM
      BASIS_SET DZVP-MOLOPT-SR-GTH-q1
      POTENTIAL ${potential_H}
    &END KIND
    &KIND C  # CARBON ATOM
      BASIS_SET DZVP-MOLOPT-SR-GTH-q4
      POTENTIAL ${potential_C}
    &END KIND
  &END SUBSYS
 &END FORCE_EVAL


&MOTION
 &MD
  ANGVEL_TOL 1E-4
  COMVEL_TOL 1E-5
  ENSEMBLE \${ENSEMBLE_TYPE}    
  TEMPERATURE [K] $j
  STEPS 40000
  TIMESTEP [fs] 0.25
  &THERMOSTAT
    TYPE NOSE
    &NOSE ON
    &END NOSE
  &END THERMOSTAT

  &PRINT
    &CENTER_OF_MASS
      &EACH
        MD 5000
      &END EACH
    &END CENTER_OF_MASS
  &END PRINT
 &END MD

 &PRINT
   &TRAJECTORY
     &EACH
       MD 1
     &END EACH
   &END TRAJECTORY
   &VELOCITIES OFF
   &END VELOCITIES
   &FORCES OFF
   &END FORCES
   &RESTART_HISTORY
     &EACH
       MD 20000
     &END EACH
   &END RESTART_HISTORY
   &RESTART
     BACKUP_COPIES 3
     &EACH
       MD 1
     &END EACH
   &END RESTART
 &END PRINT

&END MOTION
" > ${2}-${j}k-${1}-$i.inp

########### JOB SUBMISSION & QUEUE SYSTEM ################

	if [ "$3" == 'PBS' ]; then
	    echo "PBS server detected ! Submitting ..."
	    echo "#!/bin/bash

#PBS -N ${2}-${j}-${1}-$i
#PBS -r n
#PBS -j oe
#PBS -M abb58@pitt.edu
#PBS -q dist_big
#PBS -l walltime=144:00:00,nodes=4:ppn=16

cd \$PBS_O_WORKDIR
module purge
module load cp2k/2.6.x-mvapich2

IN=${2}-${j}k-${1}-$i.inp
OUT=${2}-${j}k-${1}-$i.out

export OMP_NUM_THREADS=1
ulimit -s unlimited

prun --bind-to core cp2k.popt -i $IN > $OUT
exit 0
" > job.pbs
	    
#	    qsub job.pbs

	elif [ "$3" == 'SBATCH' ]; then
	    echo "#!/bin/bash

#SBATCH --job-name=${2}-${j}-${1}-$i
#SBATCH --nodes=2
#SBATCH --tasks-per-node=20
#SBATCH --error=${2}-${j}k-${1}-%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=abb58@pitt.edu
#SBATCH --qos=long
#SBATCH --time=144:00:00

source /etc/profile.d/spack.sh
spack load cp2k@2.6.x^mvapich2

IN=${2}-${j}k-${1}-$i.inp
OUT=${2}-${j}k-${1}-$i.out

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
ulimit -s unlimited

srun --cpu_bind=cores cp2k.popt -i \$IN > \$OUT
" > job.sbatch
	    sbatch job.sbatch

	else
	    echo "INVALID job server detected ! Purging ..."
	    exit 1;
	fi

	cd ../
    done
    cd ../
done

exit 0