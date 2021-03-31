#!/usr/local/bin/python3
import requests
import re

def getDate(string, pattern=None):
        Regex = '(\d{4}-\d{2}-\d{2})'
        pattern = re.compile(Regex)
        group = pattern.search(string)

        if group:
            date_string = group.groups()[0]
            #print("[match] :",date_string)
            return date_string 
        else:
            print("[Oops Empty] \n")
            return ''
        
def getPlatform(string):
    if "android" in string:
        return "android"
    elif "ios" in string:
        return "ios"
    elif "pulse" in string:
        return "pulse"
    
    else:
        return ""

def getVersion(string):
        Regex = '(\d+\.\d+)'
        pattern = re.compile(Regex)
        group = pattern.search(string)

        if group:
            version_string = group.groups()[0]
            #print("[match] :",version_string)
            return version_string 
        else:
            print("[Oops Empty] \n")
            return ''

def getPage(string):
        Regex = '(page\/\d+)'
        pattern = re.compile(Regex)
        group = pattern.search(string)

        if group:
            temp_string = group.groups()[0]
            page = temp_string.split('/')[-1]
            #print("[match] :",page)
            return page 
        else:
            print("[Oops Empty] \n")
            return ''