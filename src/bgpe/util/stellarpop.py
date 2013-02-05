'''
Created on Dec 10, 2012

@author: william
'''

import numpy as np
import matplotlib.pyplot as plt

class n_component: # Define a N-component SFH vector.

    def __init__(self,ages):
        self.ages = ages
        #Calculate distances between ages components
        DeltaT = (ages[1:]-ages[:-1])/2
        #Eval left and right side of each element of the base
        left = np.insert(DeltaT,0,0)
        right = np.append(DeltaT,0)
        #Eval start and end of each element of the base
        self.ages_start = ages - left
        self.ages_end = ages + right
        self.individual_sfh_curves = [] # Here we will append one by one the ugly components...
        self._total_M_fraction = 0.0 # Will be used to store the total mass fraction of each component to be used afterwards on the normalization.
    
    def _square(self, t0, l):
        #Set an array with all the elements between t0 and t0+l to 1
        mf_ = np.zeros_like(self.ages)
        mf_[np.bitwise_and(self.ages_end>=t0,self.ages_start<=(t0+l))] = 1
        args = np.argwhere(mf_ == 1)
        #Deal with the boundaries
        #lower
        mf_[args[0]] = (self.ages_end[mf_ == 1][0] - t0)/(self.ages_end[mf_ == 1][0] - self.ages_start[mf_ == 1][0])
        #upper
        if len(args) > 1: mf_[args[-1]] = (t0+l - self.ages_start[mf_ == 1][-1])/(self.ages_end[mf_ == 1][-1]-self.ages_start[mf_ == 1][-1])
        # Total Mass
        Ms = np.trapz(mf_,self.ages)
#        Ms = np.sum(mf_ * (self.ages_start - self.ages_end))
        return mf_/Ms
        
    def _exp(self, t_eb, tau):
        mf_ = np.zeros_like(self.ages)
        for i_age in range(len(self.ages)):
            if t_eb > self.ages_start[i_age]:
                if t_eb >= self.ages_end[i_age]:
                    mf_[i_age] = tau * ( np.exp((self.ages_end[i_age] - t_eb)/tau) - np.exp((self.ages_start[i_age] - t_eb)/tau) )
                elif t_eb < self.ages_end[i_age]:
                    mf_[i_age] = tau * ( 1 - np.exp((self.ages_start[i_age] - t_eb)/tau) )
#        mf_[self.ages<=t_eb] = np.exp((self.ages-t_eb)/tau)
#        # Total mass
        Me = np.trapz(mf_,self.ages)
        return mf_/Me
    
    def add_exp(self, t_eb, tau, frac):
        self.individual_sfh_curves.append(self._exp(t_eb, tau) * frac)
        self._total_M_fraction += frac

    def add_square(self, t0, l, frac, t_max = None):
        if t_max:
            square = self._square(t0, l)
            square[self.ages > t_max] = 0.0
            self.individual_sfh_curves.append(square/np.trapz(square,self.ages) * frac)
        else:
            self.individual_sfh_curves.append(self._square(t0, l) * frac)
        self._total_M_fraction += frac

    def get_sfh(self):
        sfh = np.sum(self.individual_sfh_curves, axis=0)
        sfh = sfh/np.trapz(sfh, self.ages)
        
        return sfh        

    def plot(self, log=True):
        plt.figure(1)
        plt.clf()
        if log:
            x = np.log10(self.ages)
        else:
            x = self.ages
        for i_sfh in range(len(self.individual_sfh_curves)):
            plt.plot(x, self.individual_sfh_curves[i_sfh], label = 'Curve %s' % np.int(i_sfh))
        plt.plot(x, self.get_sfh(), label = 'Total SFH curve')
        plt.legend()