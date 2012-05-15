#!/bin/bash
#export PYTHONPATH=$PYTHONPATH:/home/william/Documents/workspace/bgpe/src/
#cd /home/william/Documents/workspace/bgpe/src/
#python  bgpe/io/starlight_hdf5convert.py -d DR7 -b BS -st /net/Starlight_SDSS/DR7/input/\
#		-sd /net/Starlight_SDSS/DR7/output/Base.BC03.S/ \
#		-i /net/data_astro/william/new_catalogs/inputfile_all2hdf5.txt \
#		-o /net/data_astro/william/new_catalogs/BScat_32.hdf5
		
export PYTHONPATH=$PYTHONPATH:/home/william/Documents/workspace/bgpe/src/
cd /home/william/Documents/workspace/bgpe/src/
python  bgpe/io/starlight_hdf5convert.py -d DR7 -b BS -st /net/Starlight_SDSS/DR7/input/\
		-sd /net/Starlight_SDSS/DR7/output/Base.BC03.S/ \
		-i /net/data_astro/william/new_catalogs/inputfile_1khdf5.txt \
		-o /net/data_astro/william/new_catalogs/BScat_1k.hdf5