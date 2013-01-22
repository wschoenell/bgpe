'''
Created on Feb 23, 2012

@author: william
'''

import os
import numpy as np
import h5py
import atpy

from bgpe.core.exceptions import ReadFilterException

class readfilterset(object):
    '''
    This class reads a filterset from file and returns a "filter" object.
    '''
    
    def __init__(self):
        pass
    
    def read(self, filterfile, path=None):  
        '''
        Read filterfile
        
        Parameters
        ----------
        filterfile : string
                     Filter filename
        path : string, optional
               Path to the filterset in the filterfile (only used to .hdf5 tables)
        
        Examples
        --------
                   
        See Also
        --------
        
        Notes
        -----
        '''
        
        if not os.path.exists(filterfile):
            raise Exception('File not found: %s' % filterfile)
    
        if filterfile.endswith('.hdf5'):
            db_f = h5py.File(filterfile, 'r')
            aux_db = db_f.get(path)
            
            for filter_id in aux_db.keys():
                aux_filter = db_f.get('%s/%s' % (path, filter_id))
                aux_fid = []
                for i in range(len(aux_filter)):
                    aux_fid.append(filter_id)
                aux = atpy.Table()
                aux.add_column(name = 'ID_filter', data = aux_fid)
                aux.add_column(name = 'wl', data = aux_filter['wl'])
                aux.add_column(name = 'transm', data = aux_filter['transm'])
                if filter_id == aux_db.keys()[0]:
                    self.filterset = aux.data
                else:
                    self.filterset = np.append(self.filterset, np.array(aux.data, dtype=self.filterset.dtype))
                
        elif filterfile.endswith('.filter'):
            dt = np.dtype ([('ID_filter', 'S20'), ('wl', 'f'), ('transm', 'f')])
            self.filterset = np.loadtxt(filterfile, dtype=dt)
              
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