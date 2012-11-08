'''
Created on Oct 9, 2012

@author: william
'''

import numpy as np

def chi2(m_o, m_l, w):
    mask = (m_o == np.inf) + (m_l == np.inf) + (w == 0)
    mask = np.invert(mask)
    n_good = np.sum(mask)
    w2 = np.power(w[mask],2)
#    print 'a>', m_o
#    print 'b>', m_l
#    print 'c>', w2
#    print 'd>', mask
    s = np.sum( w2 * (m_o[mask] - m_l[mask]) ) / np.sum( w2 ) # Scaling-factor = - 2.5 log M_\star
    chi2 = np.sum( np.power(m_o[mask] - m_l[mask] - s,2) * w2 ) / np.sum(w2)
    
    return n_good, s, chi2