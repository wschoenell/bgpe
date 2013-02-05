'''
Created on Dec 10, 2012

@author: william
'''

from bgpe.util.stellarpop import n_component

import numpy as np

if __name__ == '__main__':
    ages = 10**np.arange(6,10,.01)
    model = n_component(ages)
    t0 = 10**6.5
    l = 10**5.5
    t_eb = 10**7.25
    tau = 10**7.0
    frac = 0.9
    model.add_exp(t_eb, tau, frac)
    model.add_square(t0, l, 1-frac )
    model.plot()