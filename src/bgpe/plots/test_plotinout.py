'''
Created on Nov 20, 2012

@author: william
'''

import numpy as np
import matplotlib.pyplot as plt

from bgpe.io.readsummaries import Summaries
from bgpe.io.readlibrary import Library

from bgpe.plots.labels import aux_name_props, prop_labels #FIXME: Temporal. This should come from an XML file!


summary_file = '/Users/william/Downloads/databases/stats_1k_0.01.hdf5'
obj_file = '/Users/william/Downloads/databases/database_JPAS51_OB.hdf5' #FIXME: This should come from summary_file

obj = Library(obj_file)
summaries = Summaries(summary_file)
summaries.get_path(summaries.list_paths()[-1])

summary_size = summaries.AVG.shape[1]

# stats_ds[i_f_L, i_obj,prop]


for prop in summaries.properties:
    if np.invert(prop.startswith('F') or prop.startswith('Mcor') or prop.startswith('z')):
        print '@>', prop 
        std_vec = []
        for i_f_L in range(len(summaries.f_L)):
            
            #### Calculate prop if needed. 
            if aux_name_props[prop]['eval']:
                aux_prop_obj = obj.properties[:summary_size][aux_name_props[prop]['ratio'][0][0]]/obj.properties[:summary_size][aux_name_props[prop]['ratio'][1][0]]
                if aux_name_props[prop]['log']:
                    aux_prop_obj = np.log10(aux_prop_obj)
                aux_prop_obj[np.bitwise_or(np.isnan(aux_prop_obj),np.isinf(aux_prop_obj))] = -999
            elif aux_name_props[prop]['log']:
                aux_prop_obj = np.log10(obj.properties[prop][:summary_size])
            else:
                aux_prop_obj = obj.properties[prop][:summary_size]
            #####
            
            i_prop = np.argwhere(summaries.properties == prop)[0]

            #Deal with -999 stuff.
            i_999 = (aux_prop_obj > -998.)
            p999_lim = 50 #% 
            i_999 = np.bitwise_or(i_999, summaries.AVG[i_f_L,:,i_prop][:summary_size] > p999_lim)

            diff = aux_prop_obj[i_999] - summaries.AVG[i_f_L,:,i_prop][:summary_size][i_999]
            plt.figure(1)
            plt.clf()
            plt.plot(aux_prop_obj[i_999], diff, '.')
            plt.title('fL = %s' % summaries.f_L[i_f_L])
            avg, std = np.average(diff), np.std(diff)
            print 'diff avg, std> ', avg, std 
            std_vec.append(std)
            
            if i_f_L == 0: ylim = plt.ylim()
            else: plt.ylim(ylim)
            
            raw_input()
        
        plt.figure(2)
        plt.clf()
        plt.plot(summaries.f_L, std_vec)
        armin = np.argmin(std_vec)
        plt.plot(summaries.f_L[armin], std_vec[armin], '.', color='red', label = '%d - %3.2f' % (summaries.f_L[armin], std_vec[armin]))
        plt.legend()
        try:
            plt.title(prop_labels[prop])
        except:
            plt.title(prop)
        
        plt.savefig(prop, type='png')