#!/usr/bin/python3
import requests
from lxml import html
import re
from collections import namedtuple
import pickle

import CookieHelp
import HtmlParser
import RegexHelp

class Report:
    # Static data structure , single crash shares same url template 
    host_url='https://android-crashes.prod.booking.com/crash/'
    platform_url_temp = 'https://android-crashes.prod.booking.com/crash/{platform}' 
    daily_url_temp ='https://android-crashes.prod.booking.com/crash/daily/{daily}/{platform}'
    version_url_temp ='https://android-crashes.prod.booking.com/crash/report/{daily}/{version}/{platform}/page/1'

    def __init__(self, platform='android'):
        self.platform = platform 
        self.platform_url = self.platform_url_temp.format(platform=platform)
        self.htmlcontent = None
        self.timestamp = None # default set to date(today) ?

    # https://android-crashes.prod.booking.com/crash/android
    def get_platform_url(self, platform='android'):
        return self.platform_url

    # https://android-crashes.prod.booking.com/crash/daily/2021-03-23/ios
    def get_daily_url(self, timestamp):
        Regex = '(\d{4}-\d{2}-\d{2})'
        pattern = re.compile(Regex) 

        if not pattern.search(timestamp):
            raise Exception("timestamp should be in \'2022-02-22\' format ")

        self.timestamp=timestamp

        daily_url = self.daily_url_temp.format(platform=self.platform, daily=self.timestamp)
        return daily_url

    # https://android-crashes.prod.booking.com/crash/report/2021-03-22/26.5-all/android/page/1
    def get_version_url(self, timestamp, version, platform=None):
        Regex = '(\d{4}-\d{2}-\d{2})'
        pattern = re.compile(Regex) 

        if not pattern.search(timestamp):
            raise Exception("timestamp should be in \'2022-02-22\' format ")

        self.timestamp=timestamp
        self.version_url = self.version_url_temp.format(daily=self.timestamp, platform=self.platform, version=version)
        return self.version_url

    # https://android-crashes.prod.booking.com/crash/ios
    # get all available dates on which crashes is accessable on crash frontpage  
    def get_available_dates(self,platform_url=None):
        Regex = '(\d{4}-\d{2}-\d{2})'
        pattern = re.compile(Regex)
        platform_url = platform_url or self.platform_url
        # get Html source 
        pageHtml = HtmlParser.Html(platform_url)
        date_list = pageHtml.getText(pattern)
        self.date_list = date_list
        return self.date_list

    # https://android-crashes.prod.booking.com/crash/daily/2021-03-23/ios 
    # [TODO] version is timestamp sensitive 
    # [TODO][2021-04-06][Bugs] version reporting from this func is fix ?
    def get_available_version(self,daily_url):
        Regex = '(\d+\.\d+)'
        pattern = re.compile(Regex)
        # get Html source 
        pageHtml = HtmlParser.Html(url=daily_url)
        version_list = pageHtml.getText(pattern)
        return version_list

    # check (date,version) pair makes sense - make sure at date given , expected version is released already 
    def get_all_reports(self,timestamp=None):
        if timestamp:
            Regex = '(\d{4}-\d{2}-\d{2})'
            pattern = re.compile(Regex) 

            if not pattern.search(timestamp):
                raise Exception("timestamp should be in \'2022-02-22\' format ")
        else:
            timestamp = self.timestamp

        all_reports_url = []
        daily_url = self.get_daily_url(timestamp)        
        version_list = self.get_available_version(daily_url)
        for v in version_list:
            print("version:", v)
            v_url = self.get_version_url(timestamp=timestamp, version=v)
            all_reports_url.append(v_url)
        
        if not len(version_list):
            print("No Version Detected on ", timestamp)
        return all_reports_url 


'''
[Calling instruct]
>>> import URLParser
>>> C=URLParser.Crashes()
>>> C.get_max_pages()
>>> page_urls_list=C.get_page_urls_list()
>>> for url in page_urls_list : C.get_pageHtml_cache(url)
>>> C.get_crash_elements()
>>> C.get_crash_elements_detail()
'''

#crash_url_debug = "https://android-crashes.prod.booking.com/crash/report/2021-03-23/26.5/android/page/1"

# need page number to locate url contains crash element
crash_element_info = namedtuple('crash_element_info',['element','pnum'])  
crash_elements_detail = namedtuple('crash_elements_detail',['timestamp','platform','version','crash_id','devices','is_new','is_oom','is_blacklisted','has_jira','crash_count','contents'])  

class Crashes:
    # assign default url : https://android-crashes.prod.booking.com/crash/report/2021-03-23/26.5/android/page/1
    page_url_temp ='https://android-crashes.prod.booking.com/crash/report/{daily}/{version}/{platform}/page/{pnum}'
    # https://android-crashes.prod.booking.com/crash/report/2021-04-08/26.7.1/5815275/android
    crash_id_url_temp = 'https://android-crashes.prod.booking.com/crash/report/{daily}/{version}/{crash_id}/{platform}'
    
    # divclass names

    #def __init__(self, url=crash_url_debug):
    def __init__(self, url):
        self.url = url
        self.timestamp = RegexHelp.getDate(url)
        self.version = RegexHelp.getVersion(url)
        self.platform = RegexHelp.getPlatform(url)
        # crash page url is at 
        self.current_page = None
        self.max_pages = 1

        # pageHtml cache 
        self.pageHtmlCache = {} 

        # crash_id_list attached per crash
        # ==> namedtuple('crash_element_info',['element','pnum'])
        self.crash_elements = [] 
        # ==> namedtuple('crash_elements_detail',['element','id','is_new', 'is_oom', 'is_blacklisted', 'has_jira', 'crash_count', 'contents'])
        self.crash_elements_detail = [] 

        # crash_id_list attached per crash
        self.crash_id_list = [] 

    def get_max_pages(self):
        # strip page info only
        url_strip_page_key= self.url.rsplit('/',1)[0]

        url = self.url
        pageHtml = HtmlParser.Html(url)
        url_list = pageHtml.getHref()

        # get page url
        page_url_str_list = []
        for u in url_list:
            if u and (url_strip_page_key in u):
                page_url_str_list.append(u)

        # get max page 
        self.max_pages = max(str(RegexHelp.getPage(u)) for u in page_url_str_list)
        return self.max_pages
        
    def get_page_urls_list(self, max_pages=None):
        max_pages = int(max_pages or self.max_pages)

        page_url_list=[]
        # range: 
        for n in range(1, max_pages+1):
            page_url_list.append( self.page_url_temp.format(daily=self.timestamp, platform=self.platform, version=self.version, pnum=n) )
        return page_url_list

    def get_pnum_url(self, pnum):
        return self.page_url_temp.format( daily=self.timestamp, platform=self.platform, version=self.version, pnum=pnum) 

    def get_pageHtml_cache(self, url):
        print("start parsing: \n\t {url}".format(url=url))

        pnum = RegexHelp.getPage(url)
        pageHtml = HtmlParser.Html(url) 
        self.pageHtmlCache[pnum] = pageHtml
        print("Page{pnum} cached \n".format(pnum=pnum) )

        return pageHtml

    # crash IDs is retreived per page url 
    def get_crash_elements(self):
        for pnum,pageHtml in self.pageHtmlCache.items():
            elements = pageHtml.getDivClass(classname="panel panel-primary crash-item active-crash-panel")

            if not elements:
                print("no crash elements on page : {url}".format(url=pageHtml.url)) 

            for ce in elements:
                # avoid dup when repeatedly calling this function 
                if ce is not None:
                    self.crash_elements.append( crash_element_info(element=ce, pnum=pnum) )


        return self.crash_elements

    # crash IDs is retreived per page url 
    def get_crash_elements_detail(self, infile=True):

        platform = self.platform
        version =  self.version
        timestamp = self.timestamp

        fname = 'crash_element_cache.txt'

        for ce in self.crash_elements:
            element = ce.element
            pnum = ce.pnum

            crash_id = element.get('id')
            is_new = element.get('is_new')
            is_oom = element.get('is_oom')
            is_blacklisted = element.get('is_blacklisted')
            has_jira = element.get('has_jira')
            crash_count = element.get('crashes')
            
            # convert "<class 'lxml.etree._ElementUnicodeResult'>" into string 
            contents = repr(self.get_crash_id_contents(crash_id=crash_id,pnum=pnum))

            # get crash device number
            devices = self.get_crash_devices(crash_id=crash_id)

            crash_element_detail_unit = crash_elements_detail(
                    timestamp = timestamp,
                    platform = platform,
                    version = self.version,
                    crash_id=crash_id,
                    is_new=is_new,
                    is_oom=is_oom,
                    is_blacklisted=is_blacklisted,
                    has_jira=has_jira,
                    crash_count=crash_count,
                    contents = contents,
                    devices = devices
                )  
            # avoid dup when repeatedly calling this function 
            self.crash_elements_detail.append(crash_element_detail_unit)

            if(infile):
                with open(fname, 'ab') as f:
                    pickle.dump(crash_element_detail_unit, f)

        return self.crash_elements_detail

    # get crash IDs list
    def get_crash_ids(self,crash_elements):
        
        if not crash_elements:
            raise Exception(" no crash elements , please check")
        for ce in crash_elements:
            self.crash_id_list.append(ce.element.get('id'))

        return self.crash_id_list

    # get each crash item's content
    def get_crash_id_contents(self, crash_id, pnum):
        pageHtml = self.pageHtmlCache[pnum] 
        crash_trace_id= crash_id.replace("crash","crash-trace")
        contents =pageHtml.getPreClassTextByID(classname="stacktrace", crash_trace_id=crash_trace_id)

        return contents

    def get_crash_devices(self, crash_id):

        c_id = crash_id.replace("crash-","")
        print(" Crash ID : {c_id}".format(c_id = c_id) )

        Regex ='(\d+) devices'
        pattern = re.compile(Regex)

        # generate crash_id url 
        pageHtml = HtmlParser.Html(self.crash_id_url_temp.format(daily=self.timestamp, platform=self.platform, version=self.version, crash_id=c_id) )
        pageHtmlString =  pageHtml.content.decode('utf-8')

        G = pattern.search(pageHtmlString)
        if G:
            devices = G.groups()[0]
        else:
            devices = 0

        return str(devices)

    '''
    # get each crash blocks data 
    def get_crash_data_object(self, crash_id):
        pass

    # TODO : match JIRA to crash element blocks 
    def get_jira_maps_to_crash(self, crash_id):
        pass
    '''
