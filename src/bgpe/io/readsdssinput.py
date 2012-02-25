'''
Created on Feb 23, 2012

@author: william
'''

import numpy as np

def Read7xt(arq_obs):
    print '@@@> Reading Starlight Input file: ', arq_obs
    dt = np.dtype ([('wl', 'float64'), ('flux', 'float64'), ('err', 'float64'), ('flag', 'float64')])
    return np.loadtxt(arq_obs, dtype = dt)