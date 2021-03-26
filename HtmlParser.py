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
        
