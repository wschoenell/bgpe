'''
Created on Feb 23, 2012

@author: william
'''

import numpy as np

class readfilterset(object):
    '''
    This class reads a filterset from file and returns an array "filter"
    with it.
    '''


    def __init__(self):
        pass
    
    def read(self):        
        try:
            dt = np.dtype ([('ID_filter', 'S20'), ('wl', 'f'), ('transm', 'f')])
            self.filter = np.loadtxt(self.filterfile, dtype=dt)
            return True
        except:
            return False #Exception here!!!
        