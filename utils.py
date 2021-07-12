#!/usr/local/bin/python3
from collections import namedtuple
import re

from dbApi import MonitorDB
from URLParser import Report,Crashes

# parse configurations 
import config_helper

#######################################
#     Glue logic to retrieve data 
#######################################

'''
# steps of calling Record

'''

class Record:
    def __init__(self, timestamp, platform='android', version=None, keyword=None):

        self.monitor = MonitorDB()
        self.reports = Report(platform)

        self.crash_element_detail_lists = []
        #self.crashes
        # record attributes 
        self.platform = platform

        Regex = '(\d{4}-\d{2}-\d{2})'
        pattern = re.compile(Regex) 
        if not pattern.search(timestamp):
            raise Exception("timestamp should be in \'2022-02-22\' format ")

        self.timestamp = timestamp # ranges ?

        self.version_list = None
        self.crash_url_list = None
        self.daily_url = None 

        # Mid Param  
        self.CrashOne = None

        # crashes filter 
        self.keyword = None
        self.owner = None
        self.team = None

        # configuration
        self.urls_json = None
        #print(" > Set crash url file as : {crashUrl} \n".format( crashUrl=self.url_from_json) )
        

    def read_from_db(self):
        pass

    def get_all_crash_url(self):
        # Get crash url from reports url
        self.daily_url = self.reports.get_daily_url(self.timestamp)
        self.version_list = self.reports.get_available_version(self.daily_url)
        
        self.crash_url_list = self.reports.get_all_reports()

        return self.crash_url_list

    def get_crash_elements_of_one_url(self, url):
        crash_element_detail_lists = []
        self.CrashOne =Crashes(url=url)
        self.CrashOne.get_max_pages()
        page_url_list = self.CrashOne.get_page_urls_list()

        try:
            for url in page_url_list:
                self.CrashOne.get_pageHtml_cache(url=url)
            self.CrashOne.get_crash_elements()

            crash_element_detail_lists = self.CrashOne.get_crash_elements_detail()
            if crash_element_detail_lists:
                self.crash_element_detail_lists.extend(crash_element_detail_lists )

        except Exception as exp:
            print("Failed to get Element exception: {exp}".format(exp=exp)) 

        return crash_element_detail_lists
    
    # call self.get_all_crash_url() first 
    def get_all_crash_elements(self, crash_url_list=None):
        '''
            url_from_file: set True , will dump all url from user configure file
            crash_url_list: set to list of urls you's like to parse
        '''
        crash_url_list = crash_url_list or self.crash_url_list 

        print(">>> Total len %d \n", len(crash_url_list))

        for url in crash_url_list:
            try:
                self.get_crash_elements_of_one_url(url=url)
            except Exception as exp:
                print("Failed on {url} with {exp}".format(url=url,exp=exp))
    '''
    ##### Re-structure it : low ##### 
    # All url listed in config files: urls.json
    # [TODO] peer of self.get_all_crash_url()  
    #        remove it to URLParser.py ? 
    def get_all_crash_elements_from_urls_json(self, urls_json=None):
        crash_elements = []
        crash_element_detail_lists = []

        self.crash_element_detail_lists = []
        # By default: file is located at current dir
        # pls offer file name only
        urls_json = urls_json or "urls.json"
        print(" Dump urls from : {urls_json} \n".format(urls_json=self.urls_json) )
        
        # parser json file 
        crash_url_list  = config_helper.UrlConfig(cfgFile=urls_json)
        
        print(">>> Total length {len} \n".format(len=len(crash_url_list)) )
        for url in crash_url_list:
            try:
                # get all crash elements first
                pageHtml = HtmlParser.Html(url)
                pnum = url.rsplit('/',1)[0]
                elements = pageHtml.getDivClass(classname="panel panel-primary crash-item active-crash-panel")
                
                crash_elements.append()

            except Exception as exp:
                print("Failed on {url} with {exp}".format(url=url,exp=exp) ) 
    '''
    def insert_crash_elements_to_db(self, keyword=None):
        self.monitor.create_table()
        self.monitor.insert_crash_elements(crash_elements_detail_list=self.crash_element_detail_lists)

    def select_crash_elements_from_db(self, keyword=None):
        self.monitor.insert_crash_elements(crash_elements_detail_list=self.crash_element_detail_lists)