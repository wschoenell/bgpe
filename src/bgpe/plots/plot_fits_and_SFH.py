'''
Created on May 11, 2012

@author: william
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from matplotlib.ticker import NullFormatter

class plot_fit_and_SFH(object):
    '''
        This class plots the world most famous cutre-like graphic the fit and SFH of Starlight.
    '''


    def __init__(self, sl_out, figure=1):
        '''
        Constructor
        '''
        self.sl_out = sl_out
        self.fig = plt.figure(figure)
    
    def set_title(self, title):
        self.axleft_upp.set_title(title)
    
    def draw_legends(self, metallicity=True, metallicityLoc=2):
        if(metallicity == True): self.axright_low.legend(loc=metallicityLoc)
    
    def plot_fig_starlight(self):
        
        self.fig.clf()
        plt.clf()
        
        #Some configurations
        #plt.rc('axes', grid=True)
        nullfmt = NullFormatter()
        Zcolor = ['magenta', 'cyan', 'blue', 'green', 'black', 'red', 'magenta', 'cyan', 'blue', 'green', 'black,', 'red']
        lim_res_low = -.29
        lim_res_upp = .99
        
        # Divide in two boxes 60% and 30% of size.
        box_left_low  = [.1, .1, .4, .2] #left, bottom, width, height
        box_left_upp  = [.1, .3, .4, .6]
        box_right_low = [.6, .1, .3, .3]
        box_right_upp = [.6, .4, .3, .3]
        
        #Create the axes
        self.axleft_low  = self.fig.add_axes(box_left_low)
        self.axleft_upp  = self.fig.add_axes(box_left_upp, sharex=self.axleft_low)
        self.axright_low = self.fig.add_axes(box_right_low)
        self.axright_upp = self.fig.add_axes(box_right_upp, sharex=self.axright_low)
        
        #.... Plots ...
        # LEFT
        ### LEFT - UPPER
        self.axleft_upp.plot(self.sl_out['out_spec']['wl'], self.sl_out['out_spec']['flux_obs'], color='blue') # Observed
        self.axleft_upp.plot(self.sl_out['out_spec']['wl'], self.sl_out['out_spec']['flux_syn'], color='red') # Synthetic
        
        np.seterr(divide='ignore') # Ignore zero-division error.
        err = np.ma.array(np.divide(1.,(self.sl_out['out_spec']['wei'])))
        self.axleft_upp.plot(self.sl_out['out_spec']['wl'][err > 0], err[err > 0], color='black') # Error 
        
        mi_ = np.min(self.sl_out['out_spec']['wl'])
        ma_ = np.max(self.sl_out['out_spec']['wl'])
        self.axleft_upp.set_xlim(mi_*0.9, ma_*1.1)
        
        ### LEFT - LOWER
        res = np.ma.array(self.sl_out['out_spec']['flux_obs'] - self.sl_out['out_spec']['flux_syn'])
        self.axleft_low.plot(self.sl_out['out_spec']['wl'], res, color='black') #All
        r_ = np.ma.masked_where(self.sl_out['out_spec']['wei'] > 0, res)
        self.axleft_low.plot(self.sl_out['out_spec']['wl'], r_, color='blue') #If wei > 0
        r_ = np.ma.masked_where(self.sl_out['out_spec']['wei'] == 0, res)
        self.axleft_low.plot(self.sl_out['out_spec']['wl'], r_, color='magenta') #If wei == 0
        self.axleft_low.set_ylim(lim_res_low, lim_res_upp)
        
        ## RIGHT
        log_age = np.log10(self.sl_out['pop'][3])
        Z = self.sl_out['pop'][4]
        xj = self.sl_out['pop'][1]
        mu_cor = self.sl_out['pop'][2]
        
        ### Define bar spacing
        d = log_age[1:] - log_age[:-1]
        Zwidth = np.min(d[d>0])
        
        ### RIGHT - UPPER
        aux_sum = np.zeros(np.shape(Z[Z == Z[0]]))
        i_color = 0
        for i_Z in np.unique(Z):
            v_ = (Z == i_Z)
            #self.axright_upp.bar(log_age[v_], xj[v_], width=Zwidth, align='center', alpha=Zalpha, color=Zcolor[i_color])
            self.axright_upp.bar(log_age[v_], xj[v_], width=Zwidth, align='center', color=Zcolor[i_color], bottom=aux_sum, label=('%3.4f' % i_Z))
            aux_sum = aux_sum + xj[v_]
            i_color = i_color+1
        
        ### RIGHT - LOWER
        aux_sum = aux_sum * 0.
        i_color = 0
        for i_Z in np.unique(Z):
            v_ = (Z == i_Z)
            #self.axright_low.bar(log_age[v_], mu_cor[v_], width=Zwidth, align='center', alpha=Zalpha, color=Zcolor[i_color])
            self.axright_low.bar(log_age[v_], mu_cor[v_], width=Zwidth, align='center', color=Zcolor[i_color], bottom=aux_sum, label=('%3.4f' % i_Z))
            aux_sum = aux_sum + mu_cor[v_]
            i_color = i_color+1
        self.axright_low.set_xlim(np.min(log_age)*.99,np.max(log_age)*1.01)
        
        
        
        #Remove undisered labels
        #self.axleft_upp.xaxis.set_major_formatter(nullfmt)
        #self.axright_upp.xaxis.set_major_formatter(nullfmt)
        #Remove last lower ytick
        self.axleft_low.set_yticks(self.axleft_low.get_yticks()[:-1])
        self.axright_low.set_yticks(self.axright_low.get_yticks()[:-1])
        
        
        
        #Axis Labels
        self.axright_low.set_xlabel('log age [yr]')
        self.axright_low.set_ylabel('$\log\ \mu_j$ [%]')
        self.axright_upp.set_ylabel('$x_j$ [%]')
        
        self.axleft_low.set_xlabel('$\lambda [\AA]$')
        self.axleft_low.set_ylabel('Residual spectrum')
        self.axleft_upp.set_ylabel('$F_\lambda [normalized]$')
        
        
        # Some fit labels...
        self.fig.text(.6,.88, '$\chi^2 =\ $'+('%3.2f' % self.sl_out['chi2']) ) 
        self.fig.text(.6,.84, 'adev = '+('%3.2f' % self.sl_out['adev']) ) 
        self.fig.text(.6,.80, '$S/N =\ $'+('%3.2f' % self.sl_out['SN_normwin']) ) 
        self.fig.text(.6,.76, '$A_V =\ $'+('%3.2f' % self.sl_out['A_V']) ) 
        self.fig.text(.6,.72, '$\sigma_\star =\ '+('%3.2f' % self.sl_out['v_d'])+'\ $km/s\t$v_\star =\ '+('%3.2f' % self.sl_out['v_0'])+'\ $km/s' ) 