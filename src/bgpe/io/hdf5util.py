'''
Created on Sep 21, 2012

@author: william
'''

import os
import time
import h5py

from bgpe.core.version import _bgpe_name_, _bgpe_version_

def inithdf5(filename):
    # Check if file exists:
    if os.path.exists(filename):
        raise Exception('Error! File %s already exists.' % filename)
    else:
    # If NOT, create it and put the default attributes
        db = h5py.File(filename, 'w')
        db.attrs['version'] = '%s version %s' % (_bgpe_name_, _bgpe_version_)
        db.attrs['utc_created'] = time.asctime(time.gmtime())
    
    return db

def read_filterhdf5(filename):
    db = h5py.File(filename, 'r')
    
    return db