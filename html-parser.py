#!/usr/local/bin/python3
import requests
from lxml import html

cookies={'_ga': 'GA1.2.993053394.1601363710', '_hjTLDTest': '1', '_hjid': 'db2bdee6-3ad2-4d0e-ac72-cb2a956ac40f', 'cors_js': '1', '_gcl_au': '1.1.715087511.1601368367', '_scid': '24df7c6a-e119-4571-a704-afff1c73800b', '_pxvid': '5aec0ff3-022e-11eb-bfdc-0242ac120005', 'bkng_prue': '1', 'uz': 'i', 'extranet_cors_js': '1', '_mkto_trk': 'id:261-NRZ-371&token:_mch-booking.com-1602483603543-17447', 'dqs_extranet_cors_js': '1', 'dqs_uz': 'i', 'dqs_bkng_expired_hint': 'eyJib29raW5nX2dsb2JhbCI6W3sibG9naW5faGludCI6Mzc2MjgzMDE2Mn1dfQ', 'dqs_bkng_sso_session': 'e30', 'navappJobRole': 'Software%20Quality%20Engineer', 'clba': '1', 'dqs_bkng': '11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbaxYXEzBEjstBn1rgglkA4EbJZS6jNNJqJY1AIyqlgSHmC1eNtIGogaiA1t0QsitnhsRpy%2BGIk8dixNMFOvalwDcIL7L8msEon9r76FBwv%2BghezMc%2FgRZEttzIoZun1aKRoKXVWQltTgDw5JuSL2xsArhRNF0ERGeq8mwnvfDxtD4WE7C%2BeD0P7hjoNGrLXEcMWGtLtA%2FWHv1ZaK94zcBTQ%3D%3D', 'lt-anonymous-id': '0.427e447d1759731a165', '_fbp': 'fb.1.1605152809870.231720178', 'zz_cook_tms_seg1': '1', 'zz_cook_tms_ed': '1', '11_srd': '%7B%22features%22%3A%5B%7B%22id%22%3A9%2C%22score%22%3A3%2C%22cg%22%3A4%2C%22name%22%3A%22button_focus_sequence%22%7D%2C%7B%22id%22%3A16%7D%5D%2C%22score%22%3A6%2C%22detected%22%3Afalse%7D', 'zz_cook_tms_hlist': '2546694', '_pin_unauth': 'dWlkPU1tTmpNelJtT1RrdE9UUXhNQzAwTURZekxXSmhaamt0TkdNM01XTXhaRFprTkRVeg', '__zlcmid': '11ejeozppn6maao', 'esadm': '02UmFuZG9tSVYkc2RlIyh9YbxZGyl9Y5%2BPMjr9%2FWtgmx1OwpncsTsBdM%2F6SexzydChvm7iA9jwamo%3D', 'dqs_esadm': '02UmFuZG9tSVYkc2RlIyh9YbxZGyl9Y5%2BPphnqQ54TxfVQHvKR10ZPiz3k1VauQ5EJzj7%2BwiEfH%2Fk%3D', 'sbkng': '01UmFuZG9tSVYkc2RlIyh9Yf0wUNn6GO95ewvWemWMhMw7j7q6d7vibd3yfutLDCV3Jy6igMNpirX3yVPqKNIIm%2FPJhXinM0r2', 'bkng_sso_ses': 'eyJib29raW5nX2dsb2JhbCI6W3siaCI6IjVqeGFoNWh6cFY2YTFSSjVpZi80ZVlvWE54enlMbGFNOG9wWll4S3g5RUEifV19', '_gid': 'GA1.2.1734550822.1611732617', 'bkng_iam_rt': 'CAESQ1JBMNZUPSifh5vfoHN1Qr-t9MDt02gUTjoOzsfgXeniAtwGtmPT_T8nI61Uu9rdei0ISD51Tfjy-yW67a-H1X2er3Y'}
# url to parse from html page
#r=requests.get(top_level_url,cookies=cookies)

# get tree/html from given url 
def getTree(host_url):
    r=requests.get(host_url,cookies=cookies)
    if(r.status_code != 200)
        print("[Error] get url error \n") 
    # transfer r.content to structure html  
    return tree = html.fromstring(r.content)

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

def get_app_version_list(host_url, platform, date):
    tree = getTree(host_url)
    url = null
    #TODO 
    return version_list

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