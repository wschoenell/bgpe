'''
Created on Jul 17, 2012

@author: william

This module defines the logging format. Adapted from chimera.
'''

import sys
import logging

# try to use fatser (C)StringIO, use slower one if not available
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO


def strException (e):

    def formatRemoteTraceback(remote_tb_lines) :
        result=[]
        result.append(" +--- Remote traceback:")
        for line in remote_tb_lines :
            if line.endswith("\n"):
                line=line[:-1]
            lines = line.split("\n")

            for line in lines :
                result.append("\n | ")
                result.append(line)

        result.append("\n +--- End of remote traceback")
        return result

def printException (e, stream=sys.stdout):

    print >> stream, ''.join(strException(e))

    if hasattr(e, 'cause') and getattr(e, 'cause') != None:
        print >> stream, "Caused by:",
        print >> stream, ''.join(e.cause)

class LogFormatter (logging.Formatter):

    def __init__ (self, fmt, datefmt):
        logging.Formatter.__init__(self, fmt, datefmt)

    def formatException (self, exc_info):
        stream = StringIO.StringIO()
        printException(exc_info[1], stream=stream)

        try:
            return stream.getvalue()
        finally:
            stream.close()
            
def setConsoleLevel (level):
    consoleHandler.setLevel(level)
            
#fmt = LogFormatter(fmt='%(asctime)s.%(msecs)d %(levelname)s %(name)s %(filename)s:%(lineno)d %(message)s',
#                       datefmt='%d-%m-%Y %H:%M:%S')
fmt = LogFormatter(fmt='%(levelname)s -- %(name)s: %(message)s',
                       datefmt='%d-%m-%Y %H:%M:%S')

root = logging.getLogger("bgpe")
root.setLevel(logging.DEBUG)
root.propagate = False

consoleHandler = logging.StreamHandler(sys.stderr)
consoleHandler.setFormatter(fmt)
consoleHandler.setLevel(logging.WARNING)
root.addHandler(consoleHandler)    
