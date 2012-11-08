'''
Created on Oct 24, 2012

@author: william

This auxiliar file, defines a set of common labels used to plot stuff
'''

prop_labels = { 'AV':'$A_V$',
                'at_flux':'$\\langle \log t_\star \\rangle_L$',
                'am_flux':'$< \log Z_\star >_L$',
                'at_mass':'$\\langle \log t_\star \\rangle_M$',
                'am_mass':'$< \log Z_\star >_M$',
                'M2L_r':'$ \log M / L_r$',
                'Mcor_gal':'$\log M_\star$',
                'El_W_3727':'$\log W_{ [ O II ] }$', #  [\AA^{-1}]
                'El_W_4861':'$\log W_{H\\beta}$',
                'El_W_5007':'$\log W_{ [ O III ] }$',
                'El_W_6563':'$\log W_{H\\alpha}$',
                'El_W_6584':'$\log W_{[ \\rm{N} II ]}$',
                'Ha':'$H_\\alpha$',
                'N2Ha':'$\log [ N II ] / H_\\alpha$',
                'O3Hb':'$\log [ O III ] / H_\\beta$',
                'HaHb':'$\log H_\\alpha / H_\\beta$',
                'S2Ha':'$\log [ S II ] / H_\\alpha$',
                'O2Hb':'$\log [ O II ] / H_\\beta$',
                'O3N2':'$\log [ O III ]/ [ N II ]$' }

prop_minmax = { 'AV': (-1.0, 2.0),
                'at_flux': (6.0, 10.5),
                'am_flux': (0.0, 2.5),
                'at_mass': (6.0, 10.5),
                'am_mass': (0.0, 2.5),
                'M2Lcor': (0.0, 6.5) }