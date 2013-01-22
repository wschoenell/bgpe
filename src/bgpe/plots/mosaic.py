'''
Created on Oct 24, 2012

@author: william
'''

import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter


def get_mosaic(n_rows, n_cols, margin_low = .1, margin_upp = .1, margin_left = .1, margin_right = .1, col_sep = .0, row_sep = .0, x_shareaxis = False, y_shareaxis = False, i_fig = None, figsize=None):
    '''
    Returns a matplotlib.figure with a mosaic of n_rows x n_cols boxes.
    
    Parameters
    ----------
    n_rows : float
             Number of rows.
    
    n_cols : float
             Number of columns.
    
    margin_low : float
                 Lower margin. Default: 0.1
    
    margin_upp : float
                 Upper margin. Default: 0.1
    
    margin_left : float
                  Left margin. Default: 0.1
    
    margin_right : float
                   Right margin. Default: 0.1
    
    col_sep : float
              Column separation. Default: 0.0
              
    row_sep : float
              Row separation. Default: 0.0
              
    x_shareaxis : bool
                  Share X axis? Default: False
                  
    y_shareaxis : bool
                  Share Y axis? Default: False
    
    i_fig : int
            Figure number. Default: None
    
    figsize : array, shape (width, height)
              Width x height in inches; defaults to rc figure.figsize.
              
    Returns
    -------
    figure : matplotlib.figure object with the mosaic
    
    Examples
    --------
    >>> fig_width_pt = 448.07378
    >>> inches_per_pt = 1.0 / 72.27
    >>> golden_mean = (np.sqrt(5) - 1.0) / 2.0
    >>> fig_width = fig_width_pt * inches_per_pt
    >>> fig_height = fig_width * golden_mean * 1.5
    >>> fig_size = (fig_width, fig_height)
    >>> fig = get_mosaic(5,2,row_sep = .03, figsize=(fig_width, 3/2*fig_height))
    >>> ax = fig.axes[0]
    >>> ax.plot(np.arange(10), np.arange(10))
               
    See Also
    -------- 
    matplotlib.figure
    
    '''

    figure = plt.figure(i_fig, figsize=figsize)
    figure.clf()
    
    
    row_totalsize = 1 - (margin_left + margin_right) # Total size to the rows
    col_totalsize = 1 - (margin_low + margin_upp) # Total size to the columns
    row_height = (row_totalsize - (n_rows-1)*row_sep)/n_rows # Size of each row (in y axis, of course)
    col_width = (col_totalsize - (n_cols-1)*col_sep)/n_cols # Size of each col (in x axis, of course)
    
    height = row_height
    width = col_width
    
    for i_row in range(1,n_rows+1):
        for i_col in range(1,n_cols+1):
            n_rect = (i_row - 1)*n_cols + i_col
            print 'Rectangle ', i_row, i_col, n_rect
            # From matplotlib.axes help:
            #`axes(rect, axisbg='w')`` where *rect* = [left, bottom, width, height] in normalized (0, 1) units.
            left = margin_left + (i_col - 1)*(col_width + col_sep)
            bottom = 1 - (margin_upp + i_row*row_height + (i_row-1)*row_sep)
            
            if(i_col > 1 and y_shareaxis == True):
                sharey=figure.axes[-1]
            else:
                sharey=None
            if(i_row > 1 and x_shareaxis == True):
                sharex=figure.axes[-n_cols]
            else:
                sharex=None
            
            axis = figure.add_axes([left, bottom, width, height], sharex=sharex, sharey=sharey)
            
            if(x_shareaxis == True and i_row < n_rows): axis.xaxis.set_visible(False)
            if(y_shareaxis == True and i_col > 1): axis.yaxis.set_visible(False)
            
            print 'axis = figure.add_axes([',left,', ',bottom,', ',width,', ',height,'])'
            
    return figure