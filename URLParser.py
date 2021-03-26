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
    def get_available_version(self,daily_url):
        Regex = '(\d+\.\d+)'
        pattern = re.compile(Regex)
        # get Html source 
        pageHtml = HtmlParser.Html(daily_url)
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



        