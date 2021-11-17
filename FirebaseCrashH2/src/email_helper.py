# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import dblib

bookingApp = {
	'android':'android:com.booking',
	'ios':'ios:com.booking.BookingApp',
	'default': 'not-there'
}
MAX_DISPLAY_NOTIFY = 5+1

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
        print("[in email_helper:::booking_send_email ]")
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
        print("[End email_helper:::booking_send_email ]")

    def booking_send_slack(self, sender, receiver, msgBody):
        requestUrl = "https://notifications.booking.com/api/v1/notify/slack"
        print("[in email_helper:::booking_send_slack ]")
        try:
            postBody = '''{"channel_name": "''' + receiver + '''","text":"''' + msgBody + '''","username":"''' + sender + '''"}'''
            resp = requests.post(url=requestUrl, data=postBody.encode('utf-8'), verify=False)
            print(resp)
        except Exception as e:
            print("error when sending message")
        print("[End email_helper:::booking_send_slack ]")

    def booking_send_workplace_group(self, receiver, msgBody):
        requestUrl = "https://notifications.booking.com/api/v1/notify/workplace_group_chat"

        try:
            postBody = '''{"thread_key": "''' + receiver + '''","message":"''' + msgBody + '''"}'''
            resp = requests.post(url=requestUrl, data=postBody.encode('utf-8'), verify=False)
            print(resp)
        except Exception as e:
            print("error when sending message")

class Report:
	#[android]https://console.firebase.google.com/u/0/project/booking-oauth/crashlytics/app/android:com.booking/issues/{issue_id}?time=last-seven-days
	# {bookingApp} android:com.booking 
	#[ios]"https://console.firebase.google.com/u/0/project/booking-oauth/crashlytics/app/ios:com.booking.BookingApp/issues/{issue_id}?time=last-twenty-four-hours"
	# {bookingApp} ios:com.booking.BookingApp 
	### {timeslot}last-twenty-four-hours
	url_crashlist_template = "https://firebase-app-crash.dqs.booking.com/crashdetail_user/{userconfig_id}/"
	url_firebase_template = "https://console.firebase.google.com/u/0/project/booking-oauth/crashlytics/app/{bookingApp}/issues/{issue_id}?time={timeslot}"
	url_userconfig_template = 'https://firebase-app-crash.dqs.booking.com/config/{userconfig_id}/'
	url_ignore_issue_id_template = 'https://firebase-app-crash.dqs.booking.com/crashdetail_user/{userconfig_id}/ignore-issue-id/{issue_id}/'
	mydb=dblib.DB(database='chinaqa',acc_mode='rw',user='crashmonitorbotfire_chinaqa_rw0',password='Ugzdq7E3PDzJ1wBp')
	# default db 

	# pass database as parameters
	SELECT_ISSUE_ID_LIST_IN_USERCONFIG='''
		SELECT * 
		FROM {userconfig_table}
		WHERE id={config_id}
	'''	
	GET_CRASHISSUE_CONTENT_SQLCMD = '''
		select * from `{crash_table}` where issue_id= '{issue_id}'
	''' 
	def __init__(self,config_id, mydb=None):
		if mydb:
			self.mydb = mydb
		self.url_crashlist= self.url_crashlist_template.format(userconfig_id=config_id)
		self.url_userconfig = self.url_userconfig_template.format(userconfig_id=config_id)
		# issue_id, title , crash_count, user_total, app_version	
		self.report_issue_content= []
		self.userconfig_table='userconfig_config'
		self.crash_table='CrashIssues'
		self.order_issue = False 
		self.config_id = config_id

		try:
			self.select_issue_id_list_in_userconfig = self.SELECT_ISSUE_ID_LIST_IN_USERCONFIG.format(
												userconfig_table=self.userconfig_table,
												config_id=self.config_id
												)
		except Exception as e:
			print("[Exceptions] :",str(e))
			print(" >>> select_issue_id_list_in_userconfig content: ", self.select_issue_id_list_in_userconfig)

		try:
			self.curs=self.mydb.execute(self.select_issue_id_list_in_userconfig)
			self.userconfig = self.curs.fetchone()
			self.id=self.userconfig['id']
			self.team=self.userconfig['team']
			self.platform=self.userconfig['platform']
			self.issue_id_list=self.userconfig['issue_id_list']
			self.issue_id_blacklist=self.userconfig['issue_id_blacklist']
		except Exception as e:
			print("[Exceptions] :",str(e))
			print(" >>> self.userconfig content: ", self.userconfig)

		# exclude ignore issue id
		issue_id_blacklist_set = set(self.issue_id_blacklist.split(','))
		issue_id_list_set = set(self.issue_id_list.split(','))
		self.notify_issue_list=list(issue_id_list_set-issue_id_blacklist_set)

		self.total_issue_count=len(self.notify_issue_list)

		# get bookingApp / timeslot , generate url template
		self.bookingApp = bookingApp[self.platform.lower()]
		print("[bookingApp] platform:",self.platform,self.bookingApp)
		self.timeslot = 'last-twenty-four-hours'

		# check total issue_id < 3 then display all ; >3 need to order them based on crash		
		if self.total_issue_count > 5:
			self.order_issue = True

	def get_report_issue_content(self):
		self.report_issue_content = []
		#for issue_id in self.issue_id_list.split(",")[:5]:
		for issue_id in self.notify_issue_list:
			self.get_crashissue_content_sqlcmd=self.GET_CRASHISSUE_CONTENT_SQLCMD.format(
							crash_table=self.crash_table,
							issue_id=issue_id
						)
			self.curs=self.mydb.execute(self.get_crashissue_content_sqlcmd)
			try:
				self.report_issue_content.append(self.curs.fetchone())
			except:
				print("[Abort Issue ID]", issue_id)
				continue
		return self.report_issue_content

	def generateNotificationMsg(self):
		if not self.report_issue_content:
			self.get_report_issue_content()
		# TODO: read data in database 
		msg = ""	
		# order issue by user count 
		msg = '<h2>[{platform}] has \"{count}\" Issues Detected for \"{team}\" during {timeslot}</h2>'.format(
										platform=self.platform, 
										count=self.total_issue_count, 
										team=self.team,
										timeslot = 'last-7-days'
										)
		#for issue in issue_list 
		#msg = '<H4>    issue_title    |    issue_id    |crash_count|total_user|app_version|</H4>'
		for i in self.report_issue_content[:MAX_DISPLAY_NOTIFY]:
			url_firebase = self.url_firebase_template.format(
				issue_id=i['issue_id'],	
				bookingApp=self.bookingApp,
				timeslot=self.timeslot	
			)
			#<a href='{url_crashlist}'>Detail</a>
			msg = msg + '''<H4><a href='{url_firebase}'>{issue_title}</a>\
				\n>{issue_subtitle}\
				\n>crash {crash_count} times,affects {total_user} users,\
				\n>lastest failure on {app_version} total fail on {version_count} versions<\H4>'''.format(
											issue_title=i['issue_title'],
											issue_subtitle=i['issue_subtitle'],
											issue_id=i['issue_id'],
											crash_count=i['crash_count'],
											total_user=i['total_user'],
											app_version=i['app_version'].split(',')[0],
											version_count=len(i['app_version_list'].split(',')),
											url_firebase=url_firebase,
											)
		# if total_issue > 3 
		msg = msg + '''[Notes] Crashes retrieved based on you(team) <a href='{url_userconfig}'>configurations</a>\
			\n>If you want to unsubscribe some crashes above please go <a href='<{url_crashlist}'>Here</a>\
			\n>and click *Ignore* btn'''.format(url_crashlist=self.url_crashlist,url_userconfig=self.url_userconfig)
		msg = msg + '---------------------------------------------------\\n'
		return msg
	
	def generateSlackMsg(self):
		if not self.report_issue_content:
			self.get_report_issue_content()
		# TODO: read data in database 
		msg = ""	
		'''
		if len(self.report_issue_content) == 0:
			return msg
		'''
		# order issue by user count 
		msg = '*[{platform}]* has *{count}* Issues Detected for *{team}* during {timeslot}\\n'.format(
										platform=self.platform, 
										count=self.total_issue_count, 
										team=self.team,
										timeslot = 'last-7-days'
										)
		#for issue in issue_list 
		#msg = msg + '*    issue_subtitle    |    issue_id    |crash_count|total_user|app_version    *\\n'
		for i in self.report_issue_content[:MAX_DISPLAY_NOTIFY]:
			print("['app_version']:",i['app_version'],len(i['app_version'].split(',')))
			url_ignore_issue_id = self.url_ignore_issue_id_template.format(
				issue_id=i['issue_id'],	
				userconfig_id=self.config_id
			)
			url_firebase = self.url_firebase_template.format(
				issue_id=i['issue_id'],	
				bookingApp=self.bookingApp,
				timeslot=self.timeslot	
			)
			msg = msg + '<{url_firebase}|{issue_title}>\
						\\n>{issue_subtitle}\
						\\n>crash *{crash_count}* times,affects *{total_user}* users,\
						\\n>lastest failure on *{app_version}* total fail on {version_count} versions\\n\
						\\n><{url_ignore_issue_id}|IgnoreIssue>'.format(
													issue_title=i['issue_title'],
													issue_subtitle=i['issue_subtitle'],
													issue_id=i['issue_id'],
													crash_count=i['crash_count'],
													total_user=i['total_user'],
													app_version=i['app_version'].split(',')[0],
													version_count=len(i['app_version_list'].split(',')),
													url_firebase=url_firebase,
													# btn to ignore issue id in slack 
													url_ignore_issue_id=url_ignore_issue_id,
													)
		# if total_issue > 3 
		msg = msg + '*[Notes]* Crashes retrieved based on you(team) <{url_userconfig}|configurations>\
			\\n>If you want to unsubscribe some crashes above please go <{url_crashlist}|Here>\
			\\n>and click *Ignore* btn\\n'.format(url_crashlist=self.url_crashlist,url_userconfig=self.url_userconfig)
		msg = msg + '---------------------------------------------------\\n'

		print("*****************\n",msg,"******************\n")
		#bookingValue = "Think Customer First. Own it. ------Booking Value"
		#msg = msg + bookingValue
		return msg