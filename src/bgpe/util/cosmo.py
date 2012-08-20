'''
Created on Aug 13, 2012

@author: william
'''

import numpy as np

def zcor(spec, toz, fromz=0.0):
    ''' Shift a spectrum from one to another redshift.
        Arguments:
        spec: Spectrum
              Keywords:
              wl: Wavelength (in Angstroms!)
              flux: Flux on a given wl
              error: Flux error. (Optional)
        toz: Redshift in which we want the output spectrum
        fromz: ACTUAL redshift of the spectra (default: 0.0, rest-frame)
    '''
    s = np.copy(spec)
    k = (1.+toz)/(1.+fromz)
    s['wl'] = s['wl'] * k
    k = np.power(1./k,3)
    s['flux'] = s['flux'] * k
    if('error' in s.dtype.names):
        s['flux'] = spec['flux'] * k
    return s