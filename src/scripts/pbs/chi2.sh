#!/bin/bash
#PBS -l mem=12g,ncpus=8
#PBS -q infinity
export PYTHONPATH=$PYTHON_PATH:/home/william/Documents/workspace/bgpe/src/:/home/william/Documents/workspace/pystarlight/src/

export db=$HOME

#/usr/bin/python Documents/workspace/bgpe/src/scripts/testchi2.py
rm testchi2.hdf5
time /usr/bin/python Documents/workspace/bgpe/src/scripts/chi2fit.py -i $db/database_JPAS51_OB.hdf5 -l $db/database_JPAS51_BA.hdf5 -f JPAS_51 -c 1 -o testchi2.hdf5  -v -t 6 -z 0.03 -N 1000
