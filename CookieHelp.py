#!/usr/local/bin/python3
from http.cookies import SimpleCookie

class Cookie:

    def __init__(self):
        self.cookie_string='bkng_iam_rt=CAESQ1JBTUBQH8XxERi6le8xVFEbjNsocZrFLUhF6cE2D6_MDy1GHq0a8iPh13V9u8hurnJzcqGMTMtFQXCmmUACIaEQziE'
        self.cookie=SimpleCookie()
        self.cookies =  None

    # assign any cookie_string 
    def get(self, cookie_string=None):
        self.cookie_string = cookie_string or self.cookie_string

        self.cookie.load(self.cookie_string)

        self.cookies={key: value.value  for key, value in self.cookie.items()}       

        return self.cookies