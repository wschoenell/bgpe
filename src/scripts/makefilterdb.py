'''
Created on Sep 20, 2012

@author: william

This program converts a .filter asciitable to a hdf5 filter database.
The file organization follows the schema:
/FilterSet/CCD/Filter_ID
Where Filter_ID is a table with Wavelength (in \AA) versus Transmission (in arbitrary units).

Usage:
python makefilterdb.py filterdbfile.hdf5 FilterSet.CCD1.filter FilterSet.CCD2.filter ... FilterSet.CCD#.filter

CAUTION! The filename MUST have this naming standard in order to script work well. 
'''

import os
import sys
import time
import h5py
import atpy

import numpy as np

from bgpe.io.readfilterset import readfilterset
from bgpe.io.hdf5util import inithdf5

if __name__ == '__main__' and len(sys.argv) > 2:

    dbfile = sys.argv[1]
    # Init file
    db = inithdf5(dbfile)

    
    for filter_file in sys.argv[2:]:
        aux_id = os.path.basename(filter_file).split('.')
        f = readfilterset()
        f.read(filter_file) 
        for fid in np.unique(f.filterset['ID_filter']):
            dataset = '/%s/%s/%s' % (aux_id[0], aux_id[1] ,fid)
            print dataset
            aux = atpy.Table(name = fid)
            aux.add_column(name='wl', data = f.filterset['wl'][f.filterset['ID_filter'] == fid])
            aux.add_column(name='transm', data = f.filterset['transm'][f.filterset['ID_filter'] == fid])
            db.create_dataset(dataset, data = aux.data)
        
        
    db.close()

else:
    print 'Usage: %s filterdbfile.hdf5 FilterSet.CCD1.filter FilterSet.CCD2.filter ... FilterSet.CCD#.filter' % sys.argv[0]