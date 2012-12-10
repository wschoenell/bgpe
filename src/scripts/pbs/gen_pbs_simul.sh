#!/bin/bash

for z in `seq 0.01 0.05 .5`;
do
	echo "#!/bin/bash
#PBS -l walltime=72:00:00
#PBS -l mem=8g,ncpus=1
export PYTHONPATH=$PYTHON_PATH:$HOME/Documents/workspace/bgpe/src/:$HOME/Documents/workspace/pystarlight/src/
	
export db=$HOME/databases/

#stdbuf -i0 -o0 -e0 python $HOME/Documents/workspace/bgpe/src/scripts/chi2fit.py -i \$db/database_JPAS51_OB.hdf5 -l \$db/database_JPAS51_BA.hdf5 -f JPAS_51 -c 1 -o chi2_10_$z.hdf5  -v -z $z -N 10 >> chi2_$z.log
stdbuf -i0 -o0 -e0 python $HOME/Documents/workspace/bgpe/src/scripts/chi2fit.py -i \$db/database_JPAS51_OB.hdf5 -l \$db/database_JPAS51_BA.hdf5 -f JPAS_51 -c 1 -o chi2_1k_$z.hdf5  -v -z $z -N 1000 >> chi2_$z.log" > simul_z_$z.sh

done