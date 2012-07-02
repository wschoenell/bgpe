'''
Created on Feb 23, 2012

@author: william
'''

import sys
import time
import argparse
import string as st
import numpy as np
import datetime
import h5py
import atpy

import pystarlight.io.starlighttable #io.starlighttable #@UnusedImport

from bgpe.core.exceptions import HDF5dbException
from bgpe.core.version import _bgpe_name_, _bgpe_version_

class starlightout2hdf5(object):
    def __init__(self, sdss_txt_dir, starlight_txt_dir, db_file, starlight_version='starlightv4', compression=9):
        self.starlight_version = starlight_version
        self.compression = compression
        self.db_file = db_file
        self.sdss_txt_dir = sdss_txt_dir
        self.starlight_txt_dir = starlight_txt_dir
        
    def readstarlightoutput(self, starlight_file):
        try:
            #self.starlight_output = ReadStarlightFile(self.starlight_txt_dir+starlight_file)
            self.starlight_output = atpy.TableSet(self.starlight_txt_dir+starlight_file, type=self.starlight_version)
        except:
            raise HDF5dbException('Could not read Starlight file %s' % self.starlight_txt_dir+starlight_file)
        self.starlight_file = starlight_file 
        
        
    def readsdssinput(self, sdss_file):
        try:
            #self.sdss_input = Read7xt(self.sdss_txt_dir+sdss_file)
            self.sdss_input = atpy.TableSet(self.sdss_txt_dir+sdss_file, type='starlight_input').tables['starlight_input'].data
            self.sdss_file = sdss_file
        except:
            raise HDF5dbException('Could not read SDSS file %s' % self.sdss_txt_dir+sdss_file)

    
    def createslihgtdbfile(self, db_file, dr, base):
        '''
            Creates a new starlight db_file with the dataset structure:    
                /data_release/input/plate.mjd.fiberID
                /data_release/output/base/plate.mjd.fiberID
        '''
        
        #Create a new HDF5 file:
        try:
            self.db = h5py.File(db_file, 'w')
        except:
            raise HDF5dbException('Could not create HDF5 file %s' % db_file)
        
        self.dr = dr
        self.base = base
        
        #Put some information on the base
        self.db.attrs['version'] = '%s version %s' % (_bgpe_name_, _bgpe_version_)
        self.db.attrs['utc_created'] = np.str(datetime.datetime.utcnow())
         
        
        #Create the Groups
        self.db.create_group('/'+np.str(dr)+'/input/')  #Input
        self.db.create_group('/'+np.str(dr)+'/output/'+np.str(base)+'/')  #Input
        
        
    def savetoslightdb(self):
        '''
            Save content of both input and the output files in an HDF5 file (database)
        '''
        
        f_ = st.splitfields(self.sdss_file, '.')
        
        # Save SDSS .txt inputfile:
        try:
            self.dataset = self.db.create_dataset( ('/%s/input/%s.%s.%s' % (self.dr, f_[0], f_[1], f_[2])),
                                                  data = self.sdss_input, compression=self.compression)
        except:
            raise HDF5dbException('Could not create field to %s.%s.%s. Duplicate entries on the input?'
                            % ( f_[0], f_[1], f_[2] ) )
        
        # Save Starlight .txt outputfile:
        try:
            self.dataset = self.db.create_dataset( ('/%s/output/%s/%s.%s.%s' % (self.dr, self.base, f_[0], f_[1], f_[2])),
                                                  data = self.starlight_output.spectra.data, compression=self.compression)
        except:
            raise HDF5dbException('Could not create field to %s.%s.%s. Duplicate entries on the input?'
                            % ( f_[0], f_[1], f_[2] ) )
        
        # Save the Starlight Output properties (A_V, v0, vd, ...) as dataset attributes
        for key, value in self.starlight_output.keywords.items():
            if (key != 'pop') and (key != 'out_spec'): self.dataset.attrs[key] = value
            
    
    def closeslightdb(self):
        self.db.close()
        

def argparser():
    
    ''' Defines the input and help options of the program... '''
    
    parser = argparse.ArgumentParser(description='Convert SDSS + Starlight output to a hdf5 db of spectra.')
    
    parser.add_argument('-i', metavar='inputfilelist.txt', type=str, nargs=1,
                        help='Input file list with 2 columns: SDSS and Starlight files', required=True)    
    parser.add_argument('-sd', metavar='/path/to/starlight_directory', type=str, nargs=1,
                        help='The directory where Starlight Output files are stored', required=True)
    parser.add_argument('-st', metavar='/path/to/sdss_directory', type=str, nargs=1,
                        help='The directory where SDSS .txt files are stored', required=True)
    parser.add_argument('-b', metavar='BS', type=str, nargs=1, help='Base identifier (e.g. BS)', required=True)
    parser.add_argument('-d', metavar='DR?', type=str, nargs=1, help='SDSS Data Release (e.g. DR7)', required=True)
    parser.add_argument('-o', metavar='database.hdf5', type=str, nargs=1, help='Database output file', required=True)
    parser.add_argument('--version', action='version', version='%s version %s' % (_bgpe_name_, _bgpe_version_))
    
    args = parser.parse_args()
    return args


def main(argv):
    time_start = time.time()
    args = argparser()

    ''' Read filelist (filelist should have 2 columns: sdss_file, starlight_file '''
    
    print '@> Reading file %s' % args.i[0]
    try:
        filelist = np.loadtxt(args.i[0], dtype=np.dtype([('sdss_file', 'S60'), ('starlight_file', 'S60')]))
    except:
        print 'error' # deal with this exception
    print '@> Done!' 
    
    
    txt2hdf5 = starlightout2hdf5(args.st[0], args.sd[0], args.o[0])
    
    #Create db
    txt2hdf5.createslihgtdbfile(args.o[0], args.d[0], args.b[0])
    
    for i in range(len(filelist)):
        #Read sdss_file
        txt2hdf5.readsdssinput(filelist[i]['sdss_file'])
        #Read starlight_file
        txt2hdf5.readstarlightoutput(filelist[i]['starlight_file'])
        #Write to DB
        txt2hdf5.savetoslightdb()
    #Close DB
    txt2hdf5.closeslightdb()
    print 'DONE! Total time: %3.4f seconds' % (time.time() - time_start)
    