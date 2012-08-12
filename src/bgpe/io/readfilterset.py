'''
Created on Feb 23, 2012

@author: william
'''

import numpy as np

from bgpe.core.exceptions import ReadFilterException

class readfilterset(object):
    '''
        This class reads a filterset from file and returns an array "filter"
        with it.
    '''
    
    def __init__(self):
        pass
    
    def read(self, filterfile):        
        try:
            dt = np.dtype ([('ID_filter', 'S20'), ('wl', 'f'), ('transm', 'f')])
            self.filterset = np.loadtxt(filterfile, dtype=dt)
        except:
            raise ReadFilterException('Cannot read filterfile %s' % filterfile)
        
    def calc_filteravgwls(self):
        avg = []
        for fid in np.unique(self.filterset['ID_filter']):
            avg.append(np.average(self.filterset[self.filterset['ID_filter'] == fid]['wl']))
        self.filteravgwls = np.array(avg)