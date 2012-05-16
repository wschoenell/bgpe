'''
Created on Feb 23, 2012

@author: william
'''

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
    
    StarlightOut['arq_read'] = filename

    if(just_spec == False):
    
        ## Some input info

        StarlightOut['arq_spec']    = np.str(data[5].split()[0])
        StarlightOut['arq_base']    = np.str(data[6].split()[0])
        StarlightOut['arq_masks']    = np.str(data[7].split()[0])
        StarlightOut['arq_config']  = np.str(data[8].split()[0])
        StarlightOut['N_base']        =    np.int(data[9].split()[0])
        StarlightOut['N_YAV_components']  =    np.int(data[10].split()[0])
        StarlightOut['iFitPowerLaw']      =    np.int(data[11].split()[0])
        StarlightOut['alpha_PowerLaw']    =  np.float32(data[12].split()[0])
        StarlightOut['red_law_option']    = np.str(data[13].split()[0])
        StarlightOut['q_norm']            =  np.float32(data[14].split()[0])

        ## (Re)Sampling Parameters

        StarlightOut['l_ini']           = np.float32(data[17].split()[0])
        StarlightOut['l_fin']           = np.float32(data[18].split()[0])
        StarlightOut['dl']              = np.float32(data[19].split()[0])

        ## Normalization info

        StarlightOut['l_norm']          = np.float32(data[22].split()[0])
        StarlightOut['llow_norm']       = np.float32(data[23].split()[0])
        StarlightOut['lupp_norm']       = np.float32(data[24].split()[0])
        StarlightOut['fobs_norm']       = np.float32(data[25].split()[0])

        ## S/N

        StarlightOut['llow_SN']         = np.float32(data[28].split()[0])
        StarlightOut['lupp_SN']         = np.float32(data[29].split()[0])
        StarlightOut['SN_snwin']        = np.float32(data[30].split()[0])
        StarlightOut['SN_normwin']      = np.float32(data[31].split()[0])
        StarlightOut['SNerr_snwin']     = np.float32(data[32].split()[0])
        StarlightOut['SNerr_normwin']   = np.float32(data[33].split()[0])
        StarlightOut['fscale_chi2']     = np.float32(data[34].split()[0])

        ## etc...

        StarlightOut['idum_orig']       = np.int(data[37].split()[0])
        StarlightOut['NOl_eff']         = np.int(data[38].split()[0])
        StarlightOut['Nl_eff']          = np.int(data[39].split()[0])
        StarlightOut['Ntot_clipped']    = np.int(data[40].split()[0])
        StarlightOut['Nglobal_steps']   = np.int(data[41].split()[0])
        StarlightOut['N_chains']        = np.int(data[42].split()[0])
        StarlightOut['NEX0s_base']      = np.int(data[43].split()[0])

        ## Synthesis Results - Best model ##

        StarlightOut['chi2']            = np.float32(data[49].split()[0])
        StarlightOut['adev']            = np.float32(data[50].split()[0])

        StarlightOut['sum_x']           = np.float32(data[52].split()[0])
        StarlightOut['Flux_tot']        = np.float32(data[53].split()[0])
        StarlightOut['Mini_tot']        = np.float32(data[54].split()[0])
        StarlightOut['Mcor_tot']        = np.float32(data[55].split()[0])

        StarlightOut['v_0']             = np.float32(data[57].split()[0])
        StarlightOut['v_d']             = np.float32(data[58].split()[0])
        StarlightOut['A_V']             = np.float32(data[59].split()[0])
        StarlightOut['YA_V']            = np.float32(data[60].split()[0])


        # Read/define x, mu_ini, mu_cor, age_base, Z_base & YAV_flag arrays.
        _nlast = 62+StarlightOut['N_base']
        pop = []
        for i in range(63,_nlast+1):
            #popx 2 popmu_ini 3 popmu_cor 4 popage_base 5 popZ_base 6  popYAV_flag 8 popMstars 9
            pop.append([np.float32(data[i].split()[1]),np.float32(data[i].split()[2]),np.float32(data[i].split()[3]),np.float32(data[i].split()[4]),np.float32(data[i].split()[5]),np.int(data[i].split()[7]),np.float32(data[i].split()[8])])
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
        StarlightOut['N_base']        =    np.int(data[9].split()[0])
        StarlightOut['fobs_norm']   = np.float32(data[25].split()[0])

        
    # Read spectra (l_obs, f_obs, f_syn & f_wei)
    #l_obs 1 f_obs 2 f_syn 3 f_wei 4 Best_f_SSP 5
    iaux1 = 62 + StarlightOut['N_base'] + 5 + StarlightOut['N_base'] + 2 + StarlightOut['N_base'] + 11
    StarlightOut['Nl_obs'] = np.int(data[iaux1].split()[0])
    iaux2 = iaux1 + 1
    #iaux3 = iaux1 + StarlightOut['Nl_obs']

    try:
        dt = np.dtype([('wl', 'float32'), ('flux_obs', 'float32'), ('flux_syn', 'float32'), ('wei', 'float32'), ('Best_f_SSP', 'float32')])
        out_spec = np.loadtxt(filename, dtype=dt, skiprows=iaux2)
    except:
        dt = np.dtype([('wl', 'float32'), ('flux_obs', 'float32'), ('flux_syn', 'float32'), ('wei', 'float32')])
        out_spec = np.loadtxt(filename, dtype=dt, skiprows=iaux2)
    
    StarlightOut['out_spec'] = out_spec
    
    return StarlightOut