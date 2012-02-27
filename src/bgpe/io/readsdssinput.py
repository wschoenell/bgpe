'''
Created on Feb 23, 2012

@author: william
'''

import numpy as np

def Read7xt(arq_obs):
    print '@@@> Reading Starlight Input file: ', arq_obs
    dt = np.dtype ([('wl', 'float32'), ('flux', 'float32'), ('err', 'float32'), ('flag', 'float32')])
    return np.loadtxt(arq_obs, dtype = dt)