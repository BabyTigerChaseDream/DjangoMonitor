#!/usr/local/bin/python3
import urllib.request 
import requests
from http.cookies import SimpleCookie

#from urllib.request import urlopen
#from urllib.request import HTTPPasswordMgrWithDefaultRealm

# password & username configure
# TODO
#username = "jiaguo"
#password = "secret"

header = {'Content-Type': 'text/html; charset=UTF-8'}
top_level_url = "https://android-crashes.prod.booking.com/crash/"

# user input parameter :
#date = // date format: 2021-03-02 
#platform = 

# version = -> get from url webpage 

# create a password manager
# password manager
#password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

### M1
'''
password_mgr.add_password(None, top_level_url, username, password)
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib.request.build_opener(handler)
# use the opener to fetch a URL
opener.open(top_level_url)
# Install the opener.
# Now all calls to urllib.request.urlopen use our opener.
urllib.request.install_opener(opener)

#urlstring= urlopen(top_level_url).read().decode('utf-8')
#print(urlstring)
'''
### M2
#r = requests.post(top_level_url, auth=(username, password))

### M3 : use cookie for access
rawdata='bkng_iam_rt=CAESQ1JB0J-xgah5W7za2qAGdxMAEHJi4yyM0ywpbYI5exzDuBMoqXTzqBrWl04q8LpM66QQvbvOfkTXXRRvb742tmm7tPk'
cookie=SimpleCookie()
cookie.load(rawdata)

cookies={key: value.value  for key, value in cookie.items()}
r=requests.get(top_level_url,cookies=cookies)
r.status_code # 200 

# refer to coding notes for html parsing 

