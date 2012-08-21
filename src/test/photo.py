'''
Created on Jul 17, 2012

@author: william
'''
import os
import atpy
import logging
import numpy as np
import matplotlib.pyplot as plt

import pystarlight.io.starlighttable #io.starlighttable #@UnusedImport 

from bgpe.io.readfilterset import readfilterset
from bgpe.photometry.syntphot import photoconv
from bgpe.photometry.syntphot import spec2filterset
from bgpe.util.cosmo import zcor

from bgpe.util.constants import c_AngSec

from bgpe.core.log import setConsoleLevel
setConsoleLevel(logging.DEBUG)

f = readfilterset()
#f.read('data_example/sdss_gri.filter')
f.read('data_example/Alhambra_23.filter')
f.uniform()
f.calc_filteravgwls()

model_test_file = '%s/../../../data/test/STARLIGHT_test_output_v04.txt' % os.path.dirname(pystarlight.io.starlighttable.__file__)
tm = atpy.TableSet(model_test_file, type='starlightv4')
model_spec = np.copy(tm.spectra.data.view(dtype = np.dtype([('wl', '<f4'), ('f_obs', '<f4'), ('flux', '<f4'), ('f_wei', '<f4'), ('Best_f_SSP', '<f4')])))

obs_test_file = '%s/../../../data/test/STARLIGHT_test_input.7xt.bz2' % os.path.dirname(pystarlight.io.starlighttable.__file__)
ts = atpy.TableSet(obs_test_file, type='starlight_input')
obs_spec = np.copy(ts.starlight_input.data.view(dtype = np.dtype([('wl', '<f8'), ('flux', '<f8'), ('error', '<f8'), ('flag', '<i8')])))



model_spec['flux'] = model_spec['flux'] * tm.keywords['fobs_norm'] * 1e-17
obs_spec['flux'] = obs_spec['flux'] * 1e-17
obs_spec['error'] = obs_spec['error'] * 1e-17

#print spec2filter(filter, obs_spec, model_spec, log_level=logging.DEBUG)
plt.clf()
c = photoconv()
x = spec2filterset(f.filterset, obs_spec, model_spec, dlambda_eff = 3.0)
plt.plot(f.filteravgwls, x['m_ab'])
for z in np.arange(.1, 1, .2):
    print 'z ==', z
    O = zcor(obs_spec, z)
    M = zcor(model_spec, z)
    x = spec2filterset(f.filterset, O, M, dlambda_eff = 3.0)
    plt.plot(f.filteravgwls, x['m_ab'])
    if(z > 0.3):
        plt.plot(O['wl'], -2.5*np.log10(O['flux']*(O['wl']**2)/c_AngSec) - 48.6 , color='black', alpha=.3)
        plt.plot(M['wl'], -2.5*np.log10(M['flux']*(M['wl']**2)/c_AngSec) - 48.6 , color='blue', alpha=.3)
    raw_input()
print 'test 1'
raw_input('Enter for next test...')

print c.fromStarlight(f.filterset, ts, tm, dlambda_eff = 3.0)
print 'test 2'
raw_input('Enter for next test...')

ffile = 'data_example/748.52233.410.fits'
print c.fromSDSSfits(f.filterset, ffile)
print 'test 3'
raw_input('Enter for next test...')

fits = atpy.Table(ffile, hdu='COADD')
print c.fromSDSSfits(f.filterset, fits)
print 'test 4'
raw_input('Enter for next test...')

plt.clf()
print c.fromStarlight(f.filterset, obs_test_file, model_test_file)
plt.plot(obs_spec['wl'], obs_spec['flux'], color='blue')
plt.plot(model_spec['wl'], model_spec['flux'], color='red')

#raw_input()
#
#aux_mag = []
#aux_err = []
#obs = np.copy(obs_spec)
#print 'test error'
#for i in range(1000):
#    obs_spec['flux'] = obs['flux'] + .1* obs['flux'] * np.random.normal(size=len(obs['flux']))
#    obs_spec['error'] = obs['flux'] *.1
#    aux_mag.append(c.spec2filterset(f.filterset, obs_spec, model_spec, 0.5)['m_ab'][1])
#    aux_err.append(c.spec2filterset(f.filterset, obs_spec, model_spec, 0.5)['e_ab'][1])
    
