'''
Created on Oct 22, 2012

@author: william
'''

import h5py

from bgpe.core.exceptions import BGPEException

class Input(object):
    '''
    Reads a .hdf5 template Input photometry file. 
    '''

    def __init__(self, photo_file):
        '''
        photo_file: ...
        '''
        
        # Open HDF5 file
        try:
            self._inp =  h5py.File(photo_file, 'r')
        except IOError:
            raise BGPEException('Could not open file %s.' % photo_file)
        
        #TODO: DEF FILETYPE = bgpe.???
        
        self.filtersystems = []
        self.ccds = {}
        for fid in self._inp.keys():
            if fid != 'tables':
                self.filtersystems.append(fid)
                self.ccds[fid] = self._inp['/%s' % fid].keys()
        self.z = self._inp['/tables/properties'].value['z']
        self.properties = self._inp['/tables/properties']
        
    def get_filtersys(self, fsys, ccd = None):
        if ccd == None: ccd = self.ccds[fsys][0]
        if fsys in self.filtersystems:
#            self.filterset = self._inp['/%s/%s/filterset' % (fsys, ccd)].value
#            self.filtercurves = self._inp['/%s/%s/filtercurves' % (fsys, ccd)].value
            self.data = self._inp['/%s/%s/data' % (fsys, ccd)]
            self.path = '/%s/%s/' % (fsys, ccd)
            print 'ok'
        else:
            print ':('
    
    # TODO: Slicing???