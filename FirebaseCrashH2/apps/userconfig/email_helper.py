# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

class EmailHelper:

    def send_email(self, sender, psw, receiver, smtpserver, port,title,msgBody):
        recvList = []

        try:
            smtp = smtplib.SMTP_SSL(smtpserver, port)
        except Exception as e:
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver, port)

        smtp.login(sender, psw)

        if receiver.find(';') != -1:
            recvList = receiver.split(';')
        else:
            recvList[0] = receiver

        for recevItem in recvList:
            msg = MIMEMultipart()
            body = MIMEText(msgBody, _subtype='html', _charset='utf-8')
            msg['Subject'] = title
            msg["from"] = sender
            msg["to"] = recevItem
            msg.attach(body)
            smtp.sendmail(sender, msg["to"].split(","), msg.as_string())
            print('Test report email has been sent out !')

        smtp.quit()

    def booking_send_email(self, sender, receiver, title,msgBody):
        recvList = []
        requestUrl = "https://notifications.booking.com/api/v1/notify/email"

        if receiver.find(';') != -1:
            recvList = receiver.split(';')
        else:
            #recvList[0] = receiver
            recvList.append(receiver)

        for recevItem in recvList:
            try:
                postBody = '''{{"subject":   "{0}","text":      "{1}","send_to":   [\"{2}\"],"send_from": "{3}","content_type" : "html"}}'''.format(title, msgBody, recevItem, sender)
                requests.post(url=requestUrl, data=postBody.encode(), verify=False)
            except Exception as e:
                print("error when sending message")

    def booking_send_slack(self, sender, receiver, msgBody):
        requestUrl = "https://notifications.booking.com/api/v1/notify/slack"

        try:
            postBody = '''{"channel_name": "''' + receiver + '''","text":"''' + msgBody + '''","username":"''' + sender + '''"}'''
            resp = requests.post(url=requestUrl, data=postBody.encode('utf-8'), verify=False)
            print(resp)
        except Exception as e:
            print("error when sending message")

    def booking_send_workplace_group(self, receiver, msgBody):
        requestUrl = "https://notifications.booking.com/api/v1/notify/workplace_group_chat"

        try:
            postBody = '''{"thread_key": "''' + receiver + '''","message":"''' + msgBody + '''"}'''
            resp = requests.post(url=requestUrl, data=postBody.encode('utf-8'), verify=False)
            print(resp)
        except Exception as e:
            print("error when sending message")