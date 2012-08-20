'''
Created on Jul 17, 2012

@author: william

Test the logger
'''

import logging
import bgpe.core.log

log = logging.getLogger('bgpe.test')
bgpe.core.log.setConsoleLevel(logging.INFO)

log.warn('Warn test')
log.info('Info test')
#log.err('Err test')