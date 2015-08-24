#!/bin/bash

replicas="01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23"

for i in $replicas; do
    mkdir -p replica_$i
    cd replica_$i
    cp ../../movie/final-replica-$i.xyz ./

    echo "###########################################
############### Input file ################
###########################################
@SET CHARGE     1
@SET CUTOFF     480
@SET RELCUTOFF  60
@SET SCF_CONV   1.0E-8
@SET FUNCTIONAL PBE
@SET RUN_TYPE   ENERGY
@SET MAX_SCF    1000
@SET PROJECT    replica-$i
@SET POSITION_FILE final-replica-$i.xyz

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
    BASIS_SET_FILE_NAME /gscratch1/kjohnson/abb58/cp2k-2.6/cp2k/data/BASIS_MOLOPT
    POTENTIAL_FILE_NAME /gscratch1/kjohnson/abb58/cp2k-2.6/cp2k/data/GTH_POTENTIALS
    CHARGE              \${CHARGE}
    &MGRID
      NGRIDS     5
      CUTOFF     \${CUTOFF}
      REL_CUTOFF \${RELCUTOFF}
    &END MGRID
    &QS
      METHOD      GPW
      EPS_DEFAULT 1.0E-10
    &END QS
    &SCF
      SCF_GUESS RESTART
      EPS_SCF \${SCF_CONV}
      MAX_SCF \${MAX_SCF}
      &OUTER_SCF
        MAX_SCF 10
        EPS_SCF 1.0E-6
      &END OUTER_SCF

      &PRINT
        &RESTART OFF
          &EACH
            QS_SCF 50
          &END
          ADD_LAST NUMERIC
        &END
      &END
    &END SCF
    &XC
      &XC_FUNCTIONAL \${FUNCTIONAL}
      &END XC_FUNCTIONAL
      &VDW_POTENTIAL
        DISPERSION_FUNCTIONAL PAIR_POTENTIAL
        &PAIR_POTENTIAL
          TYPE DFTD3
          REFERENCE_FUNCTIONAL PBE
          PARAMETER_FILE_NAME /gscratch1/kjohnson/abb58/cp2k-2.6/cp2k/data/dftd3.dat
          R_CUTOFF 10.0
        &END PAIR_POTENTIAL
      &END VDW_POTENTIAL
    &END XC

    &PRINT
      &HIRSHFELD ON
      &END HIRSHFELD
      &MOMENTS OFF
	PERIODIC FALSE
      &END MOMENTS
    &END PRINT
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
      POTENTIAL GTH-PBE-q6
    &END KIND
    &KIND H  # HYDROGEN ATOM
      BASIS_SET DZVP-MOLOPT-SR-GTH-q1
      POTENTIAL GTH-PBE-q1
    &END KIND
    &KIND C  # CARBON ATOM
      BASIS_SET DZVP-MOLOPT-SR-GTH-q4
      POTENTIAL GTH-PBE-q4
    &END KIND
  &END SUBSYS
 &END FORCE_EVAL
" > spec_$i.inp

    echo "#!/bin/bash

#PBS -N H++C-VIB-$i
#PBS -r n
#PBS -j oe
#PBS -M abb58@pitt.edu
#PBS -q test
#PBS -l walltime=1:00:00,nodes=2:ppn=8


cd \$PBS_O_WORKDIR
module purge
module load cp2k/2.5.1

export OMP_NUM_THREADS=1
prun --bind-to-core cp2k.popt spec_$i.inp > SPEC-$i.out
exit 0
" > job.pbs
    qsub job.pbs

    cd ../
done

exit 0