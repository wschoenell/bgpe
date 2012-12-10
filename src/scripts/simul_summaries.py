'''
Created on Nov 13, 2012

@author: william
'''

import numpy as np
import h5py
import os, sys

from bgpe.io.readchi2 import Chi2
from bgpe.fit.stats import percentiles
from bgpe.io.readlibrary import Library

from bgpe.plots.labels import aux_name_props #FIXME: Temporal. This should come from an XML file!

db_dir = '/home/william/databases/'
#db_dir = '/Users/william/Downloads/databases/'

lib_file = '%s/database_JPAS51_BA.hdf5' % db_dir
chi2_file = '%s/chi2_1k_0.%s.hdf5' % (db_dir, sys.argv[1])
stats_file = '%s/stats_1k_0.%s.hdf5' % (db_dir, sys.argv[1])


lib = Library(lib_file)
lib.get_filtersys(lib.filtersystems [0])

chi2 = Chi2(chi2_file)
chi2.get_path(chi2.list_paths()[-1])

f_L_range = np.arange(1,30,2)
stats = {'BMX': np.int,
         'P_999': np.float,
         'AVG': np.float,
         'STD': np.float,
         'P16': np.float,
         'P50': np.float,
         'P84': np.float}

# Create stats_file and populate it with respective datasets.
try:
    os.unlink(stats_file)
except:
    print 'stats_file does not exists...'
f_stats = h5py.File(stats_file)
for i in chi2._F_.attrs.keys():
    f_stats.attrs[i] = chi2._F_.attrs[i]

f_stats.create_group('/%s' % chi2.list_paths()[-1].split('/')[1])
f_stats.create_group('/%s/%s' % (chi2.list_paths()[-1].split('/')[1], chi2.list_paths()[-1].split('/')[2]))
aux_path = '/%s/%s' % (chi2.list_paths()[-1].split('/')[1], chi2.list_paths()[-1].split('/')[2])
for stat in stats.keys():
#    aux_dtype = []
#    for aux_prop in aux_name_props.keys():
#        aux_dtype.append((aux_prop, stats[stat]))
    f_stats.create_dataset('%s/%s' % (aux_path, stat), shape=(len(f_L_range), chi2.chi2_ds.shape[0], len(aux_name_props)), dtype = stats[stat]) # stats_ds[i_f_L, i_obj,prop]
f_stats.create_dataset('/f_L', data = f_L_range)
f_stats.create_dataset('/property_labels', data = aux_name_props.keys())
stats_grp = f_stats.get(aux_path) # stats_grp[stat][i_f_L, i_obj][name_prop]
f_L_ds = f_stats.get('/f_L')

for i_f_L in range(len(f_L_range)):
    f_L = f_L_range[i_f_L]
    for i_obj in range(len(chi2.chi2_ds)): #[:2]: #FIXME:
        if i_obj % 10 == 0: print 'debug> ', f_L, i_obj
        likelihood = np.exp( - f_L * np.divide(chi2.chi2_ds[i_obj], np.subtract(chi2.n_ds[i_obj], 2) ) / 2 )
        likelihood_z = np.sum(likelihood, axis = 1)
        likelihood_T = np.sum(likelihood, axis = 0)
        for i_prop in range(len(aux_name_props)):
            name_prop = aux_name_props.keys()[i_prop]
            if aux_name_props[name_prop]['eval']:
                aux_prop_lib = lib.properties[aux_name_props[name_prop]['ratio'][0][0]]/lib.properties[aux_name_props[name_prop]['ratio'][1][0]]
                if aux_name_props[name_prop]['log']:
                    aux_prop_lib = np.log10(aux_prop_lib)
                aux_prop_lib[np.bitwise_or(np.isnan(aux_prop_lib),np.isinf(aux_prop_lib))] = -999
            elif aux_name_props[name_prop]['log']:
                aux_prop_lib = np.log10(lib.properties[name_prop])
            else:
                aux_prop_lib = lib.properties[name_prop]
            aux_999 = (aux_prop_lib > -998)
            for stat in stats.keys():
                if stat == 'BMX':
                    out = np.argmin(likelihood_T)
                elif stat == 'P_999':
                    out = np.sum(likelihood_T[np.invert(aux_999)]) / np.sum(likelihood_T)
                elif stat == 'AVG':
                    out = np.average(aux_prop_lib[aux_999], weights = likelihood_T[aux_999])
                elif stat == 'STD':
                    out = np.sqrt( np.mean( np.power(aux_prop_lib[aux_999] - np.average(aux_prop_lib[aux_999], weights = likelihood_T[aux_999]), 2) )) 
                    #np.std(aux_prop_lib[aux_999] - np.average(aux_prop_lib[aux_999], weights = likelihood_T[aux_999])) #FIXME:
                elif stat.startswith('P'):
                    p_ = np.float(stat[-2:]) / 100
                    out = percentiles(aux_prop_lib[aux_999], likelihood_T[aux_999], p_)
                
                stats_grp[stat][i_f_L, i_obj, i_prop] = out           
            
        
f_stats.close()