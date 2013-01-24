'''
Created on Nov 22, 2012

@author: william
'''

import re

import atpy
import asciitable
from atpy.asciitables import read_ascii


def read_ambcat(self, filename, header_max = 10000):
    '''
    Reads catalogs on Alberto's format.
    '''    

    self.reset()
#    self.table_name = 'catalog'
    
    self.keywords['filename'] = filename

    # Define various regular expressions...    
    is_header = re.compile('^#')
    is_section = re.compile('^##[#]+')
    div_columns = re.compile('\s*([^,\s]*)')
    div_columns_desc = re.compile('\s+')
    
    def remove_linestart(lines, start='## '):
        line_start = re.compile(start)
        for i_line in range(len(lines)):
            lines[i_line] = line_start.sub('', lines[i_line])
        return lines
        
    
    fp = open(filename)
    
    #### Get the location of multiple headers of the file ####
    i_ini = 0
    i_fin = 0
    header_divs = []
    for line in fp.readlines(header_max):
        if is_section.match(line) and i_fin > 0:
            header_divs.append([i_ini+1, i_fin-1])
            i_ini = i_fin
        i_fin += 1
        if is_header.match(line):
            i_last = i_fin
    header_divs.append([header_divs[-1][1]+2, i_last])
    fp.seek(0) # Seek to the begging of the file...
    lines = fp.readlines(header_max)
    fp.close()
    
    header = {}
    ###### HEADER 0: Text containing catalog info #######
    i_header = 0
    l = remove_linestart(lines[header_divs[i_header][0]:header_divs[i_header][1]])
    header['catalog_info'] = ''.join(l)
    
    ###### HEADER 1: Photometric Zeropoints & BPZ corrections #######
    i_header += 1
    if not lines[header_divs[i_header][0]].startswith('## Photometric'): raise Exception('Error reading catalog %s header no. %s' % (filename, i_header))
    l = lines[header_divs[i_header][0]+1:header_divs[i_header][1]]
    aux1 = {}
    aux2 = {}
    for line in l:
        cols = div_columns.findall(line)
        aux1[cols[1]] = cols[2]
        aux2[cols[1]] = cols[3]
    header['zero_point'] = aux1
    header['zero_point_correction'] = aux2
    
    ###### HEADER 2: Galactic Extinction #######
    i_header += 1
    if not lines[header_divs[i_header][0]].startswith('## Galactic'): raise Exception('Error reading catalog %s header no. %s' % (filename, i_header))
    l = lines[header_divs[i_header][0]+1:header_divs[i_header][1]]
    aux = {}
    for line in l:
        cols = div_columns.findall(line)
        aux[cols[1]] = cols[2]
    header['extinction'] = aux
    
    ###### HEADER 3: Limiting Magnitudes #######
    i_header += 1
    if not lines[header_divs[i_header][0]].startswith('## Limiting'): raise Exception('Error reading catalog %s header no. %s' % (filename, i_header))
    l = lines[header_divs[i_header][0]+1:header_divs[i_header][1]]
    aux = {}
    for line in l:
        cols = div_columns.findall(line)
        aux[cols[1]] = cols[2]
    header['limiting_magnitudes'] = aux
    
    ###### HEADER 4: Columns Description #######
    i_header += 1
    if not lines[header_divs[i_header][0]].startswith('# '): raise Exception('Error reading catalog %s header no. %s' % (filename, i_header))
    l = lines[header_divs[i_header][0]:header_divs[i_header][1]]
    aux = {}
    for line in l:
        cols = div_columns_desc.split(line)
        try:
            aux[cols[2]] = ' '.join([c for c in cols[3:]])
        except:
            pass
    header['columns_metadata'] = aux 
    
    aux_columns = remove_linestart([lines[header_divs[i_header][1]-1]], start='#')[0].split()
    
    ################ DATA #####################
    t = atpy.Table(filename, type='ascii', names=aux_columns)
    t.table_name = 'catalog'
    self.append(t)
#    read_ascii(self, filename, names=aux_columns)
    
    ################ HEADER ###################
    for key in header.keys():
        if key == 'catalog_info':
            self.keywords[key] = header[key]
        else:
            t = atpy.Table()
            t.table_name = key
            x = []
            y = []
            for key_ in header[key].keys():
                x.append(key_)
                y.append(header[key][key_])
            t.add_column('x', x)
            t.add_column('y', y)
            self.append(t)