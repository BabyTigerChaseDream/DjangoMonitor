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
