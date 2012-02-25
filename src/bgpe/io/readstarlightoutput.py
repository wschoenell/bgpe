'''
Created on Feb 23, 2012

@author: william
'''

import shlex
import numpy as np

def ReadStarlightFile(filename, just_spec=False):
    '''
        Returns an array w/ outputfile from StarlightChains_v05 
                    (http://starlight.ufsc.br/)
    '''
    
    
    print '@@@> Reading Starlight Output file: ', filename
    fp = open(filename)
    data = fp.readlines()
    fp.close()

    StarlightOut = {}

    if(just_spec == False):
    
        ## Some input info

        StarlightOut['arq_spec']    = np.str(shlex.split(data[5])[0])
        StarlightOut['arq_base']    = np.str(shlex.split(data[6])[0])
        StarlightOut['arq_masks']    = np.str(shlex.split(data[7])[0])
        StarlightOut['arq_config']  = np.str(shlex.split(data[8])[0])
        StarlightOut['N_base']        =    np.int(shlex.split(data[9])[0])
        StarlightOut['N_YAV_components']  =    np.int(shlex.split(data[10])[0])
        StarlightOut['iFitPowerLaw']      =    np.int(shlex.split(data[11])[0])
        StarlightOut['alpha_PowerLaw']    =  np.float(shlex.split(data[12])[0])
        StarlightOut['red_law_option']    = np.str(shlex.split(data[13])[0])
        StarlightOut['q_norm']            =  np.float(shlex.split(data[14])[0])

        ## (Re)Sampling Parameters

        StarlightOut['l_ini']           = np.float(shlex.split(data[17])[0])
        StarlightOut['l_fin']           = np.float(shlex.split(data[18])[0])
        StarlightOut['dl']              = np.float(shlex.split(data[19])[0])

        ## Normalization info

        StarlightOut['l_norm']          = np.float(shlex.split(data[22])[0])
        StarlightOut['llow_norm']       = np.float(shlex.split(data[23])[0])
        StarlightOut['lupp_norm']       = np.float(shlex.split(data[24])[0])
        StarlightOut['fobs_norm']       = np.float(shlex.split(data[25])[0])

        ## S/N

        StarlightOut['llow_SN']         = np.float(shlex.split(data[28])[0])
        StarlightOut['lupp_SN']         = np.float(shlex.split(data[29])[0])
        StarlightOut['SN_snwin']        = np.float(shlex.split(data[30])[0])
        StarlightOut['SN_normwin']      = np.float(shlex.split(data[31])[0])
        StarlightOut['SNerr_snwin']     = np.float(shlex.split(data[32])[0])
        StarlightOut['SNerr_normwin']   = np.float(shlex.split(data[33])[0])
        StarlightOut['fscale_chi2']     = np.float(shlex.split(data[34])[0])

        ## etc...

        StarlightOut['idum_orig']       = np.int(shlex.split(data[37])[0])
        StarlightOut['NOl_eff']         = np.int(shlex.split(data[38])[0])
        StarlightOut['Nl_eff']          = np.int(shlex.split(data[39])[0])
        StarlightOut['Ntot_clipped']    = np.int(shlex.split(data[40])[0])
        StarlightOut['Nglobal_steps']   = np.int(shlex.split(data[41])[0])
        StarlightOut['N_chains']        = np.int(shlex.split(data[42])[0])
        StarlightOut['NEX0s_base']      = np.int(shlex.split(data[43])[0])

        ## Synthesis Results - Best model ##

        StarlightOut['chi2']            = np.float(shlex.split(data[49])[0])
        StarlightOut['adev']            = np.float(shlex.split(data[50])[0])

        StarlightOut['sum_x']           = np.float(shlex.split(data[52])[0])
        StarlightOut['Flux_tot']        = np.float(shlex.split(data[53])[0])
        StarlightOut['Mini_tot']        = np.float(shlex.split(data[54])[0])
        StarlightOut['Mcor_tot']        = np.float(shlex.split(data[55])[0])

        StarlightOut['v_0']             = np.float(shlex.split(data[57])[0])
        StarlightOut['v_d']             = np.float(shlex.split(data[58])[0])
        StarlightOut['A_V']             = np.float(shlex.split(data[59])[0])
        StarlightOut['YA_V']            = np.float(shlex.split(data[60])[0])


        # Read/define x, mu_ini, mu_cor, age_base, Z_base & YAV_flag arrays.
        _nlast = 62+StarlightOut['N_base']
        pop = []
        for i in range(63,_nlast+1):
            #popx 2 popmu_ini 3 popmu_cor 4 popage_base 5 popZ_base 6  popYAV_flag 8 popMstars 9
            pop.append([np.float(shlex.split(data[i])[1]),np.float(shlex.split(data[i])[2]),np.float(shlex.split(data[i])[3]),np.float(shlex.split(data[i])[4]),np.float(shlex.split(data[i])[5]),np.int(shlex.split(data[i])[7]),np.float(shlex.split(data[i])[8])])
        pop = np.transpose(pop)

        # Renormalize x to 100% sum!!
        pop[0] = 100.*pop[0]/np.sum(pop[0])


        # OBS: PL have age = 0 in the Starlight output file:(
        #      Here I change it so that age_PL = 5e5 yr... & Z_PL = solar
        #      This is all obsolete anyway. The built-in PL is not used anymore.
        if (int(StarlightOut['iFitPowerLaw']) > 0):
            print '@@> [Warning!] ...Fixing PL age & Z ...????? CHECK THIS ?????'
            pop[3][StarlightOut['N_base'] - 1] = 5e5 #popage_bae
            pop[4][StarlightOut['N_base'] - 1]   = 0.02 #popZ_base

        StarlightOut['pop'] = pop
    else:
        #print 'Warning: just_spec set to TRUE! Reading only the spectra.'
        StarlightOut['N_base']        =    np.int(shlex.split(data[9])[0])
        StarlightOut['fobs_norm']   = np.float(shlex.split(data[25])[0])

        
    # Read spectra (l_obs, f_obs, f_syn & f_wei)
    #l_obs 1 f_obs 2 f_syn 3 f_wei 4 Best_f_SSP 5
    iaux1 = 62 + StarlightOut['N_base'] + 5 + StarlightOut['N_base'] + 2 + StarlightOut['N_base'] + 11
    StarlightOut['Nl_obs'] = np.int(shlex.split(data[iaux1])[0])
    iaux2 = iaux1 + 1
    #iaux3 = iaux1 + StarlightOut['Nl_obs']

    
    dt = np.dtype([('wl', 'float64'), ('flux_obs', 'float64'), ('flux_syn', 'float64'), ('wei', 'float64'), ('Best_f_SSP', 'float64')])
    out_spec = np.loadtxt(filename, dtype=dt, skiprows=iaux2)
    
    StarlightOut['out_spec'] = out_spec
    
    return StarlightOut