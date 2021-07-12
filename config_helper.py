#!/usr/bin/python3
import json
import pathlib
import os 

def UrlConfig(cfgFile):
    curPath = pathlib.Path(__file__).parent.absolute()
    curPath = os.path.abspath(os.path.dirname(__file__))
    cfgFile = os.path.join(curPath,cfgFile)

    print("[Log] Parse configuration file : {cfgFile}".format(cfgFile=cfgFile))
    
    with open(cfgFile,encoding='utf-8') as f:
        urls = json.load(f)
    
    return urls


def ConfigPath(cfgFile):
    curPath = pathlib.Path(__file__).parent.absolute()

    curPath = os.path.abspath(os.path.dirname(__file__))
    print("[Log] curPath: {curPath}".format(curPath=curPath))
    
    cfgFile = os.path.join(curPath,cfgFile)
    print("[Log] cfgFile : {cfgFile}".format(cfgFile=cfgFile))