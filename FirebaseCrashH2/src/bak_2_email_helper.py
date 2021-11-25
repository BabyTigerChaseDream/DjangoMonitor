# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import dblib

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

class Report:
	url_userconfig_template = "https://firebase-app-crash.dqs.booking.com/crashdetail_user/{userconfig_id}/"
	mydb=dblib.DB(database='chinaqa',acc_mode='rw',user='crashmonitorbotfire_chinaqa_rw0',password='Ugzdq7E3PDzJ1wBp')
	# default db 

	# pass database as parameters
	SELECT_ISSUE_ID_LIST_IN_USERCONFIG='''
		SELECT id,team,platform,issue_id_list
		FROM {userconfig_table}
		WHERE id={config_id}
	'''	
	GET_CRASHISSUE_CONTENT_SQLCMD = '''
		select 
			issue_id, 
			issue_title, 
			platform,
			crash_count,
			total_user,	
			app_version
		from `{crash_table}` 
		where 
			issue_id= '{issue_id}'
	''' 
	def __init__(self,config_id, mydb=None):
		if mydb:
			self.mydb = mydb
		self.url_userconfig = self.url_userconfig_template.format(userconfig_id=config_id)
		# issue_id, title , crash_count, user_total, app_version	
		self.report_issue_content= []
		self.userconfig_table='userconfig_config'
		self.crash_table='CrashIssues'
		self.order_issue = False 
		self.config_id = config_id

		self.select_issue_id_list_in_userconfig = self.SELECT_ISSUE_ID_LIST_IN_USERCONFIG.format(
											userconfig_table=self.userconfig_table,
											config_id=self.config_id
											)
		self.curs=self.mydb.execute(self.select_issue_id_list_in_userconfig)
		self.userconfig = self.curs.fetchone()
		self.id=self.userconfig['id']
		self.team=self.userconfig['team']
		self.platform=self.userconfig['platform']
		self.issue_id_list=self.userconfig['issue_id_list']
		self.total_issue_count=len(self.issue_id_list.split(','))

		# check total issue_id < 3 then display all ; >3 need to order them based on crash		
		if self.total_issue_count > 5:
			self.order_issue = True

	def get_report_issue_content(self):
		self.report_issue_content = []
		for issue_id in self.issue_id_list.split(",")[:5]:
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
	
	def generateEmailMsg(self):
		if not self.report_issue_content:
			self.get_report_issue_content()

		if not any(self.report_issue_content):
			msg = ""
			return msg
		# order issue by user count 
		msg = '<H3>[{platform}]:\"{count}\" Crashes Detected for \"{team}\"</H3>'.format(
										platform=self.platform, 
										count=self.total_issue_count, 
										team=self.team
										)
		#for issue in issue_list 
		msg = msg + '<H4>    issue_title    |    issue_id    |crash_count|total_user|app_version|</H4>'
		for i in self.report_issue_content:
			try:
				msg = msg + '<h4>{issue_title}|{issue_id}|{crash_count}|{total_user}|{app_version}|</h4>'.format(
																		issue_title=i['issue_title'],
																		issue_id=i['issue_id'],
																		crash_count=i['crash_count'],
																		total_user=i['total_user'],
																		app_version=i['app_version'][0:20]
																		)
			except:
				print("[Exceptions]")
				print("[Issue content]",i)
				continue
		# if total_issue > 3 
		msg = msg + "<H3><br>More Crashes' <a href='{}'>Detail</a><br><br></H3>".format(self.url_userconfig)

		bookingValue = "<H3>Think Customer First. </H4><H4>Own it.</H4> <H4>------Booking Value</H3>"
		msg = msg + bookingValue
		return msg
	
	def generateSlackMsg(self):
		if not self.report_issue_content:
			self.get_report_issue_content()

		if not any(self.report_issue_content):
			msg = ""
			return msg	
		# order issue by user count 
		msg = '*[{platform}]:\"{count}\" Crashes Detected for \"{team}\"*\\n'.format(
										platform=self.platform, 
										count=self.total_issue_count, 
										team=self.team
										)
		#for issue in issue_list 
		msg = msg + '*    issue_title    |    issue_id    |crash_count|total_user|app_version    *\\n'
		for i in self.report_issue_content:
			msg = msg + '{issue_title}|{issue_id}|{crash_count}|{total_user}|{app_version}\\n'.format(
																	issue_title=i['issue_title'],
																	issue_id=i['issue_id'],
																	crash_count=i['crash_count'],
																	total_user=i['total_user'],
																	app_version=i['app_version'][0:20]
																)
		# if total_issue > 3 
		msg = msg + "*More Crashes Detail:'{}'*\\n".format(self.url_userconfig)

		bookingValue = "Think Customer First. \\n Own it.\\n------Booking Value"
		msg = msg + bookingValue
		return msg