#!/usr/local/bin/python3
import requests
from lxml import html
import re

import CookieHelp

# url to parse from html page
#r=requests.get(top_level_url,cookies=cookies)

# get tree/html from given url 
def getTree(host_url):
    r=requests.get(host_url,cookies=cookies)
    if(r.status_code != 200)
        print("[Error] get url error \n") 
    # transfer r.content to structure html  
    return tree = html.fromstring(r.content)

# host_url ='https://android-crashes.prod.booking.com/crash/'
def get_platformdaily_crash_url(host_url, user_date, user_platform):
    tree = getTree(host_url)
    url_date_platform = null

    # format input date ?
    # fetch each reference link , filter the one matches our date 
    for txpath in tree.xpath("//a"):
        href = txpath.get('href')
        if str(user_date) in href and str(user_platform) in href:
            url = href
            return url
    else
        print("[Warning] no matching url detected")
    return url

# host_url = 'https://android-crashes.prod.booking.com/crash/daily/2021-03-22/android'
def get_app_version_list(host_url, platform, date):
    tree = getTree(host_url)
    version_list = []
    for txpath in tree.xpath("//a"):
        text = txpath.text 
        # version contains digits 
        if(re.search(r'\d', text)):
            version_list.append(text)
        else:
            continue

    return version_list

# host_url = 'https://android-crashes.prod.booking.com/crash/daily/2021-03-22/android'
def get_version_crash_url(host_url, app_version):
    tree = getTree(host_url)
    url = null

    for txpath in tree.xpath("//a"):
        href = txpath.get('href')
        if str(app_version) in href:
            url = href
            return url 
    else
        print("[Warning] no matching url detected")
    return url

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

# Get total page number :
'''
def get_total_page_num_in_crash(crash_url)
    # view-source:https://android-crashes.prod.booking.com/crash/report/2021-03-23/26.5/android/page/1
    # search for test : ""Last Page"" -> grep "/page/{num}"
'''


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
        print('[DBG] crash id: ',c.get('id'))
    # regex match on id ?  
        if crashtrace_id in c.get('id') :
            crashtrace_element = c
            crashtrace_data = crashtrace_element.text_content()
            break
    else:
        print("[Info] no matching crashtrace-id found\n")
        crashtrace_id = 0

    return crashtrace_id 
    #return crashtrace_data

#def search_in_crashtrace_content()