#!/bin/bash
#PBS -l mem=8g,ncpus=1
export PYTHONPATH=$PYTHON_PATH:$HOME/Documents/workspace/bgpe/src/:$HOME/Documents/workspace/pystarlight/src/

export db=$HOME/databases/

rm testchi2.hdf5
rm testchi2_small.hdf5
#time /usr/bin/python Documents/workspace/bgpe/src/scripts/chi2fit.py -i $db/database_JPAS51_OB.hdf5 -l $db/database_JPAS51_BA.hdf5 -f JPAS_51 -c 1 -o testchi2_small.hdf5  -v -t 6 -z 0.03 -N 10
time /usr/bin/python Documents/workspace/bgpe/src/scripts/chi2fit.py -i $db/database_JPAS51_OB.hdf5 -l $db/database_JPAS51_BA.hdf5 -f JPAS_51 -c 1 -o testchi2.hdf5 -v -z 0.03 #-N 10000
