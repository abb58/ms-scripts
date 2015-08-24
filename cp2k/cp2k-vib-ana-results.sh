#!/bin/bash

# Analyze the results that got generated from 
# vibrational analysis
dirs="09 10 11"

for ii in $dirs; do
    cd replica_$ii
    perl /gscratch1/kjohnson/abb58/ms-scripts/tccl/CP2K/cp2kfreq2mov.pl vibration-$ii.out ./final-replica-$ii.xyz
    perl /gscratch1/kjohnson/abb58/ms-scripts/tccl/CP2K/cp2kfreq.pl vibration-$ii.out
    cd ../
done

exit 0