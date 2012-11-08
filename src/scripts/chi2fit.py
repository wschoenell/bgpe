#!/usr/local/bin/python2.7
# encoding: utf-8
'''
scripts.chi2fit -- Fits chi2 over a library

@author:     william
        
@license:    GPLv3

@contact:    william@iaa.es
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from bgpe.core.version import _bgpe_version_, _bgpe_updated_
from bgpe.core.exceptions import BGPECLIError

import h5py
import numpy as np

from bgpe.library.model import library
from bgpe.fit.stats import chi2

from multiprocessing import Process

DEBUG = 0
TESTRUN = 0
PROFILE = 0

def get_zslice(l, z):
    return np.copy(l.library[np.argwhere(l.z == z),:])

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % _bgpe_version_
    program_build_date = str(_bgpe_updated_)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

USAGE
''' % (program_shortdesc)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        
        parser.add_argument("-i", "--inputfile", dest="input", help="Input filename ", required=True)
        parser.add_argument("-l", "--library", dest="library", help="Template library filename ", required=True)
        parser.add_argument("-f", "--filtersystem", dest="filtersystem", help="Filtersystem ", required=True)
        parser.add_argument("-c", "--ccd", dest="ccd", help="CCD ", required=True)
        
        parser.add_argument("-o", "--outputfile", dest="output", help="Output filename ", required=True)
        
        parser.add_argument("-z", "--obj_z", dest="obj_z", type=float, help="Redshift to get on the object libfile", required=True)
        
        parser.add_argument("-N", "--Ngals_max", dest="Nmax", type=int, help="Max number of input galaxies to run over")
        
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        
        parser.add_argument("-t", "--threads", dest="nt", type=int, default=0, help="set number of threads [default: %(default)s]")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        # Process arguments
        args = parser.parse_args()
        
        if args.nt:
            print 'MP'
    
        
        if args.verbose > 0:
            print("Verbose mode on")
            
    except KeyboardInterrupt:
        print 'CTRL+C pressed... exiting...'
        return 0
    
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    

    
    inp = library(args.input)
    lib = library(args.library)
    
    inp.get_filtersys(args.filtersystem, args.ccd) # obj
    lib.get_filtersys(args.filtersystem, args.ccd) # libra
    
    
    o_list = get_zslice(inp, args.obj_z)
    if args.Nmax != None:
        o_list = o_list[:np.int(args.Nmax)]
    
    N_obj = len(o_list)
    
    try:
        f = h5py.File(args.output, mode = 'w-')
    except IOError:
        raise BGPECLIError('File %s already exists.' % args.output)
    
    # Define some auxiliar data...
    f.attrs.create('z', args.obj_z)
    f.attrs.create('ifile', args.input)
    f.attrs.create('lib', args.library)
    f.attrs.create('lib', args.library)
    f.attrs.create('version', '%s - %s' % (program_name, program_version))
    ### 
    
    aux_shape = (N_obj, lib.library.shape[0],lib.library.shape[1])
    n_ds = f.create_dataset( '%s/n' % (lib.path), shape = aux_shape, dtype = np.int)
    s_ds = f.create_dataset( '%s/s' % (lib.path), shape = aux_shape)
    chi2_ds = f.create_dataset( '%s/chi2' % (lib.path), aux_shape)
    
    if not args.nt:
        calc_chi2(N_obj, o_list, inp, lib, n_ds, s_ds, chi2_ds, args)
    else:
        p = []
        i_obj = np.array(np.linspace(0, N_obj, args.nt+1), dtype = np.int)
        for i_t in range(len(i_obj)-1):
            print (i_obj[i_t], i_obj[i_t+1]-1)
            p.append(Process(target = calc_chi2, args = ((i_obj[i_t], i_obj[i_t+1]), o_list, inp, lib, n_ds, s_ds, chi2_ds, args) ))
            p[-1].start()
            
            
        
            
    
    ###
    
    f.close()

def calc_chi2(i_objs, o_list, inp, lib, n_ds, s_ds, chi2_ds, args):
    
    if type(i_objs) == tuple:
        i_ini = i_objs[0]
        i_fin = i_objs[1]
    else:
        i_ini = 0
        i_fin = i_objs
    
    for i_obj in range(i_ini, i_fin):
        obj = o_list[i_obj]
        log_mass = inp.properties[i_obj]['Mcor_fib']
        # To a galaxy with 10^10 M\odot:
        obj['m_ab'] = -2.5 * log_mass + obj['m_ab']
        obj_err2 = np.power(obj['e_ab'], 2)
        
        N_z, N_tpl = lib.library.shape[:2]
        
        for i_z in range(N_z):
            a = get_zslice(lib, lib.z[i_z])
            for i_tpl in range(N_tpl):
                w = 1 / (obj_err2 + np.power(a[i_tpl]['e_ab'], 2))
                n_ds[i_obj,i_z,i_tpl], s_ds[i_obj,i_z,i_tpl], chi2_ds[i_obj,i_z,i_tpl] = chi2(obj['m_ab'], a[i_tpl]['m_ab'], w)
                if i_z % 5 == 0 and i_tpl == 0 and args.verbose > 0:
                    print 'DEBUG: I\'m at i_obj, i_z --> %s, %s' % (i_obj, i_z)

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'scripts.chi2fit_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
