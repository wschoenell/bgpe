'''
Created on Oct 9, 2012

@author: william
'''

import numpy as np

def chi2(m_o, m_l, w):
    '''
    Returns n_good, s and chi2 for an observed-library AB magnitude pair.
    
    Parameters
    ----------        
              
    Returns
    -------
    n_good: array_like
            Number of good pixels
    
    s: array_like
       Scaling-factor. :math:`-2.5 \\log M_\\star = {\\sum w^2(l) * \\left(m_o(l) - m_l (l) \\right)}\\over{\\sum_l w^2(l)}`
       
    
    chi2: array_like
          Chi-square. :math:`\\chi^2 = \\sum_l \\left( m_o(l) - m_l(l) - s_{lo}(l) \\right)^2 * w^2(l)`
    
    Examples
    --------
               
    See Also
    --------
    
    Notes
    -----
    '''
    mask = (m_o == np.inf) + (m_l == np.inf) + (w == 0)
    mask = np.invert(mask)
    n_good = np.sum(mask)
    w2 = np.power(w[mask],2)
#    print 'a>', m_o
#    print 'b>', m_l
#    print 'c>', w2
#    print 'd>', mask
    s = np.sum( w2 * (m_o[mask] - m_l[mask]) ) / np.sum( w2 ) # Scaling-factor = - 2.5 log M_\star
    chi2 = np.sum( np.power(m_o[mask] - m_l[mask] - s,2) * w2 )
    
    return n_good, s, chi2

def percentiles(x,y,perc):
        y = y[np.argsort(x)]
        x = np.sort(x)
        y = np.cumsum(y)
        y = y/y[-1]
        out = np.interp(perc, y, x)
        return out