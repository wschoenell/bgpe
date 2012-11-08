'''
Created on Oct 22, 2012

@author: william
'''

import h5py

from bgpe.core.exceptions import BGPEException

class library(object):
    '''
    Reads a .hdf5 template library. 
    '''

    def __init__(self, library_file):
        '''
        library_file: ...
        '''
        
        # Open HDF5 file
        try:
            self._lib =  h5py.File(library_file, 'r')
        except IOError:
            raise BGPEException('Could not open file %s.' % library_file)
        
        #TODO: DEF FILETYPE = bgpe.library
        
        self.filtersystems = []
        self.ccds = {}
        for fid in self._lib.keys():
            if fid != 'tables':
                self.filtersystems.append(fid)
                self.ccds[fid] = self._lib['/%s' % fid].keys()
        self.z = self._lib['/tables/z'].value
        self.properties = self._lib['/tables/properties']
        
    def get_filtersys(self, fsys, ccd = None):
        if ccd == None: ccd = self.ccds[fsys][0]
        if fsys in self.filtersystems:
            self.filterset = self._lib['/%s/%s/filterset' % (fsys, ccd)].value
            self.filtercurves = self._lib['/%s/%s/filtercurves' % (fsys, ccd)].value
            self.library = self._lib['/%s/%s/library' % (fsys, ccd)]
            self.path = '/%s/%s/' % (fsys, ccd)
            print 'ok'
        else:
            print ':('
    
    # TODO: Slicing???