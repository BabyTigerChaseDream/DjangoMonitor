#!/usr/local/bin/python3
import urllib.request 
# python 3.8 no longer supports requests - noted, use python3.7 here
import requests 
from http.cookies import SimpleCookie

# self-defined model
import htmlParser

header = {'Content-Type': 'text/html; charset=UTF-8'}
top_level_url = "https://android-crashes.prod.booking.com/crash/"

# user input parameter :
date = "2021-03-22"
platform = "android"
version = '26.5-all'

### use cookie for access
rawdata='bkng_iam_rt=CAESQ1JBTUBQH8XxERi6le8xVFEbjNsocZrFLUhF6cE2D6_MDy1GHq0a8iPh13V9u8hurnJzcqGMTMtFQXCmmUACIaEQziE'

cookie=SimpleCookie()
cookie.load(rawdata)

cookies={key: value.value  for key, value in cookie.items()}
r=requests.get(top_level_url,cookies=cookies)
r.status_code # 200 

# parameters to select crash item


