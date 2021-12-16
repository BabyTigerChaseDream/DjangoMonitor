# directly import Django settings DATABASE
import timelib
from datetime import datetime, timedelta 
import dblib
import email_helper

bookingApp = email_helper.bookingApp

#from django.conf import settings

# TODO : How to access Django settings variable here ?
#database = settings.DATABASES['default']['NAME']
#username = settings.DATABASES['default']['USER']
#password = settings.DATABASES['default']['PASSWORD']

database = 'chinaqa' 
username = 'crashmonitorbotfire_chinaqa_rw0'
password = 'TfFzooLSUv4SlZ8'
acc_mode = 'rw'

conn = dblib.DB().conn

# reading data from CrashIssues Database 
'''
○ Logic of weekly static generations : crash issue table -> Timestamp
	○ Time of Event  First occurred (Tf)   
	○ Time of Event first retrieved into crash monitor(Tr) 
	○ Time of Event last updated this week (Tu) 
	○ Time of Week start (Monday) (Ts)
	○ Time of Week end (Sunday?) (Te)
		§ Total New issue retrieved based on configuration:   Ts< Tr < Te
		§ Total issue ignored this week : issue in black list of configuration  and  Ts < Tr < Te
 		§ Total issue disappeared (drop out of configurations) :  Ts< Tu < Te  & Ts < Tr < Te 
'''

# API to check time stamp 
def timestamp_in_between(user_timestamp, start_time, end_time):
    if user_timestamp > start_time.strftime("%Y-%m-%d %H:%M:%S") and user_timestamp < end_time.strftime("%Y-%m-%d %H:%M:%S"):
        return True
    else:
	    return False

# weekly crashes 
class Wdata:
    # This weekly data purely depends on china qa crash monitor database
    # so we can directly use Django settings data  
	mydb=dblib.DB(database=database,acc_mode=acc_mode,user=username,password=password)
	# DQS url :
	url_crashlist_template = "https://firebase-app-crash.dqs.booking.com/crashdetail_user/{userconfig_id}/"
	url_userconfig_template = 'https://firebase-app-crash.dqs.booking.com/config/{userconfig_id}/'
	url_ignore_issue_id_template = 'https://firebase-app-crash.dqs.booking.com/crashdetail_user/{userconfig_id}/ignore-issue-id/{issue_id}/'
	url_firebase_template = "https://console.firebase.google.com/u/0/project/booking-oauth/crashlytics/app/{bookingApp}/issues/{issue_id}?time={timeslot}"
	# pass database as parameters
	SELECT_ISSUE_ID_LIST_IN_USERCONFIG='''
		SELECT * 
		FROM {userconfig_table}
		WHERE id={config_id}
	'''	
	GET_CRASHISSUE_CONTENT_SQLCMD = '''
		select * from `{crash_table}` where issue_id= '{issue_id}'
	''' 
	def __init__(self,config_id, 
                start_time=(datetime.utcnow() - timedelta(days=7)), 
                end_time=datetime.utcnow() ,
                mydb=None):
		if mydb:
			self.mydb = mydb
		self.start_time = start_time 
		self.end_time = end_time
		# stringify
		self.start_time_string = self.start_time.strftime("%Y-%m-%d")
		self.end_time_string = self.end_time.strftime("%Y-%m-%d")

		self.url_crashlist= self.url_crashlist_template.format(userconfig_id=config_id)
		self.url_userconfig = self.url_userconfig_template.format(userconfig_id=config_id)
		# issue_id, title , crash_count, user_total, app_version	
		self.report_issue_content= []
		self.userconfig_table='userconfig_config'
		self.crash_table='CrashIssuesDbg'
		self.config_id = config_id
		self.timslot = 'last-twenty-four-hours'

		try:
			self.select_issue_id_list_in_userconfig = self.SELECT_ISSUE_ID_LIST_IN_USERCONFIG.format(
												userconfig_table=self.userconfig_table,
												config_id=self.config_id
												)
		except Exception as e:
			print("[Exceptions] :",str(e))
			print(" >>> select_issue_id_list_in_userconfig content: ", self.select_issue_id_list_in_userconfig)

		try:
            # UserConfiguration info 
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

        # active issues in previous weeks & this week 
		self.total_issue_list=list(issue_id_list_set)
		self.total_active_issue_list=list(issue_id_list_set-issue_id_blacklist_set)
		self.total_ignore_issue_id=list(set(issue_id_blacklist_set)-set(['0000-0000-0000-0000']))

		self.total_issue_count=len(self.total_active_issue_list)

		# get bookingApp / timeslot , generate url template
		self.bookingApp = bookingApp[self.platform.lower()]
		print("[bookingApp] platform:",self.platform,self.bookingApp)
		timeslot = 'last week / this week'
		self.timeslot = timeslot

    # active issues newly happen this weekly 
	def get_weekly_new_issue(self):
		self.weekly_new_issue = {
           'issue_list': [],
           'issue_count': 0 
        } 

		# round#1 check active issues 
		for issue_id in self.total_issue_list:
			self.get_crashissue_content_sqlcmd=self.GET_CRASHISSUE_CONTENT_SQLCMD.format(
							crash_table=self.crash_table,
							issue_id=issue_id
						)
			self.curs=self.mydb.execute(self.get_crashissue_content_sqlcmd)
			try:
				current_issue_content = self.curs.fetchone()
				first_retrieve_timestamp = current_issue_content['first_retrieve_timestamp']
				if timestamp_in_between(user_timestamp=first_retrieve_timestamp,
                                        start_time=self.start_time,
                                        end_time=self.end_time):
					self.weekly_new_issue['issue_count'] +=1
					self.weekly_new_issue['issue_list'].append(current_issue_content['issue_id'])
			except Exception as e:
				print("[Exception]", e)
				print("[Abort Issue ID]", issue_id)
				continue

		return self.weekly_new_issue

    # active issues being ignored this weekly 
	def get_weekly_ignore_issue(self):
		self.weekly_ignore_issue = {
           'issue_list': [],
           'issue_count': 0 
        } 
		for issue_id in self.total_ignore_issue_id:
			self.get_crashissue_content_sqlcmd=self.GET_CRASHISSUE_CONTENT_SQLCMD.format(
							crash_table=self.crash_table,
							issue_id=issue_id
						)
			self.curs=self.mydb.execute(self.get_crashissue_content_sqlcmd)
			try:
				current_issue_content = self.curs.fetchone()
				first_retrieve_timestamp = current_issue_content['first_retrieve_timestamp']
				if timestamp_in_between(user_timestamp=first_retrieve_timestamp,
                                        start_time=self.start_time,
                                        end_time=self.end_time):
					self.weekly_ignore_issue['issue_count'] +=1
					self.weekly_ignore_issue['issue_list'].append(current_issue_content['issue_id'])
			except Exception as e:
				print("[Exception]", e)
				print("[Abort Issue ID]", issue_id)
				continue

		return self.weekly_ignore_issue

    # issues newly happen this weekly but later disappeared 
	def get_weekly_itermittant_issue(self):
		self.weekly_itermittant_issue = {
           'issue_list': [],
           'issue_count': 0 
        } 
		#for issue_id in self.issue_id_list.split(",")[:5]:
		for issue_id in self.total_issue_list:
			self.get_crashissue_content_sqlcmd=self.GET_CRASHISSUE_CONTENT_SQLCMD.format(
							crash_table=self.crash_table,
							issue_id=issue_id
						)
			self.curs=self.mydb.execute(self.get_crashissue_content_sqlcmd)
			try:
				current_issue_content = self.curs.fetchone()
				first_retrieve_timestamp = current_issue_content['first_retrieve_timestamp'] 
				if timestamp_in_between(user_timestamp=first_retrieve_timestamp,
                                        start_time=self.start_time,
                                        # if issue is intermittant : it was not updated last time 
                                        end_time=self.end_time - timedelta(days=1)):
					self.weekly_itermittant_issue['issue_count'] +=1
					self.weekly_itermittant_issue['issue_list'].append(current_issue_content['issue_id'])
			except Exception as e:
				print("[Exception]", e)
				print("[Abort Issue ID]", issue_id)
				continue
		return self.weekly_itermittant_issue

	def generateWeeklyEmailMsg(self):
	#	if not self.report_issue_content:
 	#  		self.get_report_issue_content()
	#	# TODO: read data in database 
	#	msg = ""	
	#	
	#	if self.total_issue_count == 0:
	#		print('Weekly: generateWeeklyEmailMsg Empty Content\n')
	#		msg = '<h3>Good Job, no crashes detected for configuration  {team} , we will continue monitoring</h3>'.format(
	#			team=self.team	
	#		)

	#		msg = msg + "<h3>NO Crashes retrieved based on you(team) <a href='{url_userconfig}'>configurations</a></h3>\
	#			<h3>We will continue monitoring crashes for you </h3>\
	#			<h3>Feel Free to adjust the configurations <a href='{url_userconfig}'>Here</a></h3>".format(url_userconfig=self.url_userconfig)
	#	else:
	#		print('Weekly: generateWeeklyEmailMsg NA Empty Content\n')
	#		# order issue by user count 
	#		msg = '<h2>[{platform}] has {count} Issues Detected for {team} during {timeslot}</h2>'.format(
	#										platform=self.platform, 
	#										count=self.total_issue_count, 
	#										team=self.team,
	#										timeslot = timeslot
	#										)
	#		# if total_issue > 3
	#		msg = msg + "<h3>Crashes retrieved based on you(team) <a href='{url_userconfig}'>configurations</a></h3>\
	#			<h3>If you want to unsubscribe some crashes above please go <a href='{url_crashlist}'>Here</a></h3>\
	#			<h3>and click Ignore btn</h3>".format(url_crashlist=self.url_crashlist,url_userconfig=self.url_userconfig)

	#	print("[Email Message] >>>> \n",msg)
	#	print("[Email End]>>>>>>>>>>>>>>>>>>>>> \n",msg)
	#	return msg 
		pass
	
	def generateWeeklySlackMsg(self):
		msg = ""	
		if len(self.total_active_issue_list) == 0:
			print('generateWeeklySlackMsg Empty Content\n')
			msg = ':memo: Week `{start_time_string} to {end_time_string}` Report for *{team}* on *[{platform}]* :\
       			   \\nGood Job, *NO* *active* crashes detected for your configuration we will continue monitoring\
       			'.format(
						platform=self.platform, 
						team=self.team,
						start_time_string =  self.start_time_string,
						end_time_string = self.end_time_string,
					)

			msg = msg + '\\n>*[Notes]* NO Crashes retrieved based on you(team) <{url_userconfig}|configurations>\
				\\n>If you want to modify crash monitor configurations please go <{url_userconfig}|Here>\
				\\n>and click Update btn\\n'.format(url_userconfig=self.url_userconfig)
		else:
			print('Weekly: generateWeeklySlackMsg NA Empty Content\n')
			# order issue by user count 
			msg = ':memo: Week `{start_time_string} to {end_time_string}` Report for *{team}* on *[{platform}]* :\
       				\\n>Ignored Issues `issues still active but ignored by you`: *{ignore_count}* \
       				\\n>Intermittant issues `issues met user configurations intermittantly`: *{intermittant_count}* \
       				\\n>Active Issues `issues stays active and you are monitoring`: *{active_count}* \
       				\\n>Active Issues listed below: \
               		\\n>'.format(
							platform=self.platform, 
							count=self.total_issue_count, 
							team=self.team,
							start_time_string =  self.start_time_string,
							end_time_string = self.end_time_string,
							#total_count = len(self.total_issue_list),
							active_count = self.weekly_new_issue['issue_count']-self.weekly_ignore_issue['issue_count'],
							ignore_count = self.weekly_ignore_issue['issue_count'],
							intermittant_count = self.weekly_itermittant_issue['issue_count']
						)
			for issue_id in list(set(self.weekly_new_issue['issue_list']) - set(self.weekly_ignore_issue['issue_list'])):
				url_firebase = self.url_firebase_template.format(
					issue_id=issue_id,	
					bookingApp=self.bookingApp,
					timeslot=self.timeslot						
				)
				# get issue details : title 
				self.get_crashissue_content_sqlcmd=self.GET_CRASHISSUE_CONTENT_SQLCMD.format(
					crash_table=self.crash_table,
					issue_id=issue_id
				)
				self.curs=self.mydb.execute(self.get_crashissue_content_sqlcmd)
				try:
					issue_title = self.curs.fetchone()['issue_title']
				except:
					print("[Abort Issue ID]", issue_id, issue_title)
					continue

				msg = msg +'<{url_firebase}|{issue_title}>'.format(
								url_firebase = url_firebase,
								issue_title = issue_title
							) 
			# if total_issue > 3 
			msg = msg + '\\n>*[Notes]* Crashes retrieved based on you(team) <{url_userconfig}|configurations>\
				\\n>If you want to unsubscribe some crashes above please go <{url_crashlist}|Here>\
				\\n>and click *Ignore* btn\\n'.format(url_crashlist=self.url_crashlist,url_userconfig=self.url_userconfig)
			msg = msg + '---------------------------------------------------\\n'

			print("*****************\n",msg,"******************\n")
			#bookingValue = "Think Customer First. Own it. ------Booking Value"
			#msg = msg + bookingValue
		return msg
