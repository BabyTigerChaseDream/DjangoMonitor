#!/usr/local/bin/python3
import pathlib,os

#curPath = os.path.abspath(os.path.dirname(__file__))
curPath = pathlib.Path(__file__).parent.absolute()
print(curPath)

'''
class JsonHelper:

    def __init__(self, cfgFd=None):
        cfgFd = cfgFd or 'CrashUrlConfig.json' 

        curPath = os.path.abspath(os.path.dirname(__file__) )
        print( str(urPath) )  
'''