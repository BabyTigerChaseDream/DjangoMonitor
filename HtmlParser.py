#!/usr/local/bin/python3
import requests
from lxml import html
import re

import CookieHelp

HtmlCookie = CookieHelp.Cookie()


class Html:
    cookies = HtmlCookie.get()

    def __init__(self, url):
        self.url = url
        self.tree = None
        try:
            r = requests.get(self.url, cookies=self.cookies)
            r.raise_for_status()
            self.content = r.content 
            self.tree = html.fromstring(r.content)
            
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)

    def getTree(self):
        return self.tree

    def getHref(self, pattern=None):
        HrefList = []
        for t in self.tree.xpath("//a"):
            href = t.get('href')
            if pattern:
                if pattern.search(href):
                    HrefList.append(href)
                else:
                    continue
            else:
                HrefList.append(href)

        return HrefList

    def getText(self, pattern=None):
        TextList = [] 
        for t in self.tree.xpath("//a"):
            Text = t.text
            if pattern:
                if pattern.search(Text):
                    TextList.append(Text)
                else:
                    continue
            else:
                TextList.append(Text)

        return TextList

    def getDivClass(self, classname):
        ClassList = [] 
        #tree.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']")
        for t in self.tree.xpath("//div[@class='{classname}']".format(classname=classname)):
            ClassList.append(t)
        return ClassList 
    
    def getPreClassTextByID(self, classname, crash_id):
        crash_content = ''
        #tree.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']")
        for t in self.tree.xpath("//pre[@class='{classname}']".format(classname=classname)):
            print("[DBG] id is : {myid}".format(myid=t.get('id')))
            if t.get('id') == crash_id:
                crash_content = t.text_content()
                break
        else:
            #url = self.url
            raise Exception(" no crash match your ID:{crash_id} \n at {url} , please check".format(crash_id=crash_id, url=self.url))

        return crash_content 
        
