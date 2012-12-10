'''
Created on Oct 24, 2012

@author: william
'''

import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pylab

from bgpe.plots.mosaic import get_mosaic
from bgpe.io.readlibrary import Library

def plot_chi2(axis, prop, likelihood, x, x_correct, nbins = 100):
    #plt.clf()
    
    # Posterior #
    aux_hst1, aux_bins = np.histogram(x,weights=likelihood,bins=nbins, normed=True)
    left = np.array(aux_bins[:-1])
    right = np.array(aux_bins[1:])
    pts1 = left+(right-left)/2
    aux_hst1 = aux_hst1 / np.max(aux_hst1)
    
    axis.plot(pts1,aux_hst1, color='magenta')
    
    # Prior #
    aux_hst2, aux_bins = np.histogram(x, bins=nbins, normed=True)
    left = np.array(aux_bins[:-1])
    right = np.array(aux_bins[1:])
    pts2 = left+(right-left)/2
    aux_hst2 = aux_hst2 / np.max(aux_hst2)
    
    axis.plot(pts2,aux_hst2, ':', color='blue')
    
    ylim = (0., 1.01)
    axis.plot([x_correct,x_correct],ylim, color='green')
    axis.set_ylim(ylim)
    
    # Average value:
    avg = np.sum(x*likelihood)/np.sum(likelihood)
    axis.plot([avg, avg],ylim, '--', color='red')
    
    xtxt = axis.get_xlim()[0] + (axis.get_xlim()[1] - axis.get_xlim()[0]) *.03
    ytxt = .72
    
    axis.text(xtxt, ytxt, prop)
    axis.text(xtxt, ytxt-.1, '%5.3f' % (x_correct - avg))
    
#    print l1.properties['at_flux'][i_obj]
#    print l2.properties['at_flux'][np.argmin(t_prob[i_obj])]
    #raw_input()

def p999(prop, likelihood):
    return np.sum(np.sum(likelihood[prop < -998.])/np.sum(likelihood))
    
    

#####################################################################################################################

def rcLatex():
    # From http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples
    fig_width_pt = 448.07378
    inches_per_pt = 1.0 / 72.27
    golden_mean = (np.sqrt(5) - 1.0) / 2.0
    fig_width = fig_width_pt * inches_per_pt
    fig_height = fig_width * golden_mean * 1.5
    fig_size = (fig_width, fig_height)
    params = {'backend': 'ps',
              'axes.labelsize': 8,
              'text.fontsize': 6,
              'axes.titlesize': 'small',
              'legend.fontsize': 8,
              'xtick.labelsize': 8,
              'ytick.labelsize': 8,
              #'text.usetex': True,
              #'font.family': 'serif',
              'figure.subplot.hspace': .32,
              'figure.subplot.wspace': .18,
              'figure.figsize': fig_size}
    pylab.rcParams.update(params)

#####################################################################################################################

def get_zslice(l, z):
    return l.library[np.argwhere(l.z == z),:]

## Library
_dir = '/Users/william/Downloads/databases/'
f1 = _dir+'database_JPAS51_OB.hdf5'
f2 = _dir+'database_JPAS51_BA.hdf5'

l1 = Library(f1) #obj
l2 = Library(f2) #tmpl

l1.get_filtersys('JPAS_51', '1')
l2.get_filtersys('JPAS_51', '1')

##

ds_path = '/JPAS_51/1/'
h5file = _dir+'chi2_1k_0.01.hdf5'
#h5file = '../../scripts/testchi2.hdf5'

f = h5py.File(h5file)


o_list = get_zslice(l1, f.attrs.get('z'))

chi2_ds = f['/%s/chi2' % ds_path][0:100]
s_ds = f['/%s/s' % ds_path][0:100]
logM = np.divide(s_ds,-2.5)
n_ds = f['/%s/n' % ds_path][0:100]

f_L = 5.

#t_prob = np.exp( - f_L * 1000 * np.sum( np.divide(chi2_ds, n_ds) , axis = 1) / 2 )
#z_prob = np.exp( - f_L  * 1000 * np.sum( np.divide(chi2_ds, n_ds) , axis = 2) / 2 )
#likelihood = np.exp( - 1000 * f_L * np.divide(chi2_ds, n_ds) / 2 )

likelihood = np.exp( - f_L * np.divide(chi2_ds, np.subtract(n_ds, 2) ) / 2 )
#t_prob = np.exp( - f_L * np.sum( chi2_ds.value , axis = 1) / 2 )
#z_prob = np.exp( - f_L * np.sum( chi2_ds.value , axis = 2) / 2 )

t_prob = np.sum(likelihood, axis = 1)
z_prob = np.sum(likelihood, axis = 2)

#t_prob = np.exp( - np.sum( chi2_ds , axis = 1) / 2 )
#z_prob = np.exp( - np.sum( chi2_ds , axis = 2) / 2 )

plots = ['at_flux', 'A_V', 'EW_6563', 'Mcor_gal']

for i_obj in range(len(t_prob)):
    plt.clf()
    #fig = get_mosaic(2,2, i_fig = 1)
    fig = get_mosaic(3,2,row_sep = .03, i_fig = 1)
    
    ##### Redshift #####
    plot_chi2(fig.axes[0], 'z', z_prob[i_obj], l2.z, f.attrs.get('z')   , nbins = 45)
    ##### MASS #####
    logMa =  (np.sum(s_ds[i_obj] * likelihood[i_obj]) / np.sum(likelihood[i_obj])) / -2.5
    print 'logM> %s' % logMa
    plot_chi2(fig.axes[1], 'Mass', likelihood[i_obj], logM[i_obj], l1.properties['Mcor_fib'][i_obj])
    print logM[i_obj][likelihood[i_obj] == likelihood[i_obj].min()][0]
    #plot_chi2(fig.axes[1], 'Mass', t_prob[i_obj], np.sum(logM[i_obj], axis=0)/logM.shape[0], 10)
    
    for i_plot in np.array(range(len(plots)))+2:
        prop = plots[i_plot-2]
        mask = np.bitwise_and(l2.properties[prop] > -998., l2.properties[prop] < 200.)
        if prop.split('_')[0] == 'EW':
            plot_chi2(fig.axes[i_plot], prop, t_prob[i_obj][mask], np.log10(l2.properties[prop][mask]), np.log10(l1.properties[prop][i_obj]))
        else:
            plot_chi2(fig.axes[i_plot], prop, t_prob[i_obj][mask], l2.properties[prop][mask], l1.properties[prop][i_obj])
            print p999(l2.properties[prop], t_prob[i_obj])
    
    ####### Spec Plot #######
    if raw_input('Want spec plot sir?') == 'y':
        N_z = l2.library.shape[0]
        N_t = l2.library.shape[1]
        
        a = likelihood[i_obj]
        b = l2.library.value['m_ab'].copy()
        
        for i_z in range(N_z):
            for i_t in range(N_t):
                b[i_z,i_t] = b[i_z,i_t] + s_ds[i_obj,i_z,i_t] 
        
        mask = (b == np.inf)
        b_masked = b.copy()
        b_masked[mask] = 0.
        
        c = np.tensordot(a, b_masked)
        
        aux = np.ones_like(b)
        aux[mask] = 0.
        
        d = np.tensordot(a, aux)
        
        x = c/d # - 2.5 * logMa
        
        plt.figure(2)
        plt.errorbar(l1.filterset['wl_central'], o_list[i_obj]['m_ab'] - 2.5 * l1.properties['Mcor_fib'][i_obj] , yerr = o_list[i_obj]['e_ab'],color = 'blue')
        plt.plot(l1.filterset['wl_central'], x, color = 'red')
    
    #########################
    
    print 'done!'
    raw_input('Enter goes next...')
    

#figure = get_mosaic(2,2)