#!/usr/local/bin/python3
from http.cookies import SimpleCookie

class Cookie:

    def __init__(self):
        self.cookie_string='bkng_iam_rt=CAESQ1JBsEvG5RPAhDygicD074NowqLqaNCQ3F7MOckp9KcxhLwwziNKc8OEKRdMgyZKQrC75381mD82MMrrlsxkkqcy1l0'
        # CAESQ1JBE7aiDXrRNcssLzeS0CfRKB
        self.cookie=SimpleCookie()
        self.cookies =  None

    # assign any cookie_string 
    def get(self, cookie_string=None):
        self.cookie_string = cookie_string or self.cookie_string

        self.cookie.load(self.cookie_string)

        self.cookies={key: value.value  for key, value in self.cookie.items()}       

        return self.cookies