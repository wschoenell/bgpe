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
        ''' Reads filterfile '''      
        try:
            dt = np.dtype ([('ID_filter', 'S20'), ('wl', 'f'), ('transm', 'f')])
            self.filterset = np.loadtxt(filterfile, dtype=dt)
        except:
            raise ReadFilterException('Cannot read filterfile %s' % filterfile)
        
    def uniform(self, dl=1):
        ''' Interpolates filter curves to match a specific uniform lambda coverage
            Argument:
            dl: Delta lambda spacing (default: 1 Angstrom)
        '''
        aux = []
        for fid in np.unique(self.filterset['ID_filter']):
            xx = self.filterset[self.filterset['ID_filter'] == fid]
            new_lambda = np.arange(xx['wl'].min(), xx['wl'].max(), 1.0)
            new_transm = np.interp(new_lambda, xx['wl'], xx['transm'])
            for i in range(len(new_lambda)):
                aux.append((fid, new_lambda[i], new_transm[i]))
        self.filterset = np.array(aux, dtype = self.filterset.dtype)
            
        
    def calc_filteravgwls(self):
        ''' Calulates the mean wavelenght of each filter (good for plotting)'''
        avg = []
        for fid in np.unique(self.filterset['ID_filter']):
            avg.append(np.average(self.filterset[self.filterset['ID_filter'] == fid]['wl']))
        self.filteravgwls = np.array(avg)