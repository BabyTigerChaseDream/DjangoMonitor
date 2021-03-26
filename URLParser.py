#!/usr/local/bin/python3
import requests
from lxml import html
import re

import CookieHelp
import HtmlParser

class Reports:
    # Static data structure , single crash shares same url template 
    host_url='https://android-crashes.prod.booking.com/crash/'
    platform_url_temp = 'https://android-crashes.prod.booking.com/crash/{platform}' 
    daily_url_temp ='https://android-crashes.prod.booking.com/crash/daily/{daily}/{platform}'
    version_url_temp ='https://android-crashes.prod.booking.com/crash/report/{daily}/{version}/{platform}/page/1'

    def __init__(self, platform='android'):
        self.platform = platform 
        self.platform_url = platform_url_temp.format(platform=platform)
        self.htmlcontent = None

    # https://android-crashes.prod.booking.com/crash/android
    def get_platform_url(self, platform='android'):
        return self.platform_url

    # https://android-crashes.prod.booking.com/crash/daily/2021-03-23/ios
    def get_daily_url(self, timestamp):
        self.timestamp=timestamp
        daily_url = daily_url_temp.format(platform=self.platform, daily=self.timestamp)
        return daily_url

    # https://android-crashes.prod.booking.com/crash/report/2021-03-22/26.5-all/android/page/1
    def get_version_url(self, platform=None, timestamp, version):
        self.timestamp=timestamp
        self.version_url = version_url_temp.format(daily=self.timestamp, platform=self.platform, version=version)
        return self.version_url

    # https://android-crashes.prod.booking.com/crash/ios
    # get all available dates on which crashes is accessable on crash frontpage  
    def get_available_dates(self,platform_url=None):
        Regex = '(\d{4}-\d{2}-\d{2})'
        pattern = re.compile(Regex)
        platform_url = platform_url or self.platform_url
        # get Html source 
        pageHtml = HtmlParser.Html(platform_url)
        date_list = pageHtml.getHref(pattern)
        self.date_list = . date_list
        return self.date_list

    # https://android-crashes.prod.booking.com/crash/daily/2021-03-23/ios 
    def get_available_version(self,daily_url):
        Regex = '(\d+\.\d+)'
        pattern = re.compile(Regex)
        # get Html source 
        pageHtml = HtmlParser.Html(daily_url)
        version_list = pageHtml.getText(pattern)
        return version_list
        
# =========================================== #

#######################
#''' crash ID data  '''
#######################
'''
[crash_id data structure]
crash_id_list = [c for c in tree.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']")]
crash_id_list[0].keys()
['class', 'id', 'is_new', 'is_oom', 'is_blacklisted', 'has_jira', 'crashes']
'''
def get_crash_id_list(version_url, keyword=null):
    # filter: new / JIRA / blacklisted :
    # new :show_new=show-only 
    tree = getTree(version_url)
    crash_id_list = [c.get('id') for c in tree.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']")]

    if (num_crash=len(crash_id_list)):
       print("Detected %d crashes ",num_crash) 
    else:
        #crash_id_list = []
        print("[Warning] No crash ID detected")
    return crash_id_list 

'''
 GET all keys in crash_id block
 filter / keys : crash number,new,jira ...
['class', 'id', 'is_new', 'is_oom', 'is_blacklisted', 'has_jira', 'crashes']
'''
def get_crash_id_key_list(version_url, keyword=null):
    # new :show_new=show-only 
    tree = getTree(version_url)
    crash_id_key_list = []

    for c in tree.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']"):
        crash_id_key_list = c.keys()
        break
    else:
        print("no crash detected \n")

    return crash_id_key_list

''' return crashes detected on this element ''' 
def get_crash_id_crashes(crashelement, keyword=null):
    crashes = crashelement.get('crashes') 
    return int(crashes)

''' crashes ID on this element ''' 
def get_crash_id_ID(crashelement, keyword=null):
    crashid = crashelement.get('id') 
    return crashid

''' is this crashes ID new ? ''' 
def is_new_crash_id(crashelement, keyword=null):
    return (is_new = bool(crashelement.get('is_new')))

'''  has JIRA file on crashes ID ''' 
def has_jira_crash_id(crashelement, keyword=null):
    return (has_jira= bool(crashelement.get('has_jira'))

# TODO : if have JIRA , get the JIRA number 
# reference link : https://android-crashes.prod.booking.com/crash/report/2021-03-02/26.1/android/page/1
# JIRA to search : MOB-89794

'''  blacklisted this crashes ID ''' 
def is_blacklisted_crash_id(crashelement, keyword=null):
    return (is_blacklisted= bool(crashelement.get('is_blacklisted'))

'''  is_oom this crashes ID ''' 
def is_oom_crash_id(crashelement, keyword=null):
    return (is_oom= bool(crashelement.get('is_oom'))

# data temp:
crash_id="crash-{id}"
crash_trace="'crash-trace-{id}"

def get_crash_id_data(version_url, crash_id, keyword=null):
    # filter: new / JIRA / blacklisted :
    # new :show_new=show-only 
    tree = getTree(version_url)
    crash_id_list = [c for c in tree.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']")]

    return crash_data 

#############################
#''' crashtrace data  '''
#############################
''' crashtrace data : detailed crash info '''
def get_crashtrace_id_list(version_url, keyword=null):
    # filter: new / JIRA / blacklisted :
    # new :show_new=show-only 
    tree = getTree(version_url)
    crash_id_list = [c.get('id') for c in tree.xpath("//pre[@class='stacktrace']")]

    if (num_crash=len(crash_id_list)):
       print("Detected %d crashes ",num_crash) 
    else:
        #crash_id_list = []
        print("[Warning] No crash ID detected")
    return crash_id_list 

# get crashtrace data in crashtrace_id 
# - if keyword is null : simply iterate crashtrace_content & return (crashtrace_data,0)
# - if specify keywords: return (crashtrace_data, matching_id) 
def get_crashtrace_data_and_id(version_url, crashtrace_id, keyword=null):
    # filter: new / JIRA / blacklisted :
    # new :show_new=show-only 
    tree = getTree(version_url)

    crashtrace_data = False 
    
    for c in tree.xpath("//pre[@class='stacktrace']"): 
    # regex match on id ?  
        if c.get('id') == crashtrace_id:
            crashtrace_element = c
            crashtrace_data = crashtrace_element.text_content()
            break
    else:
        print("[Info] no matching crashtrace-id found\n")
        crashtrace_id = 0

    return crashtrace_id 
    #return crashtrace_data

#def search_in_crashtrace_content()