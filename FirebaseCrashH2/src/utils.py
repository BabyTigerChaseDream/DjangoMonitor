#/usr/local/bin/python3
#from FirebaseCrashH2.src.userconfig import CUser
import issues
import timelib 
import dblib
import firebase_db_common_lib 
from datetime import datetime, timedelta
import userconfig

from email_helper import EmailHelper

import jsmod
import json
import os

import schedule
import time

'''
#########################
#   API to Crash class  #
#########################
'''
#################################################################
# Configurable matrix: 
#################################################################
crash_count_max = '1000'
total_user_max = '500'
issue_count_max = '50'

table_index = 'android'
# table_index = 'iOS'
acc_mode = 'rw'

# api for user input timing 
def setup_timeslot(end_date=datetime.utcnow(), delta=7):
	return timelib.timestamp().timeslot(end_date=end_date,delta=delta)

start_timestamp_str, end_timestamp_str = setup_timeslot(end_date=datetime.utcnow(), delta=7)

# single entry to decide crash_count/total_user to retrieve !!!
def get_crash_lists(table_index, start_timestamp_str=start_timestamp_str, end_timestamp_str=end_timestamp_str, 
								crash_count_max=crash_count_max, total_user_max=total_user_max, issue_count_max=issue_count_max):
	crashes = firebase_db_common_lib.Crashes(table_index, start_timestamp_str=start_timestamp_str, end_timestamp_str=end_timestamp_str, 
								crash_count_max=crash_count_max, total_user_max=total_user_max, issue_count_max=issue_count_max)
	return crashes.get_issue_id_list()

def dump_issues(issue_id_list, filename = 'issues.json'):
	'''
	linux : python -m json.tool <file.json>
	'''
	IssueList = []
	for issue_id in issue_id_list:
		I=issues.Issue(issue_id=issue_id)
		try:
			IssueList.append(I.modelize_issue())
		except:
			print('error on issue: ',issue_id)

	print('Total issues: ', len(IssueList))

	with open(filename, 'w') as fd:
		json.dump(IssueList, fd, cls=jsmod.PythonObjectEncoder)

	print('[Issues dump to ]:', os.path.abspath(filename))

def write_issues_to_crashissue_database(issue_id_list, acc_mode, table_index, table='CrashIssuesDbg', database='chinaqa'):
	#mydb = dblib.DB(database=database,acc_mode=acc_mode)
	mydb = dblib.DB(database=database,acc_mode=acc_mode)
	#conn=mydb.connect()
	
	INSERT_ISSUE_TO_DATABASE = '''
		insert into {table}
			(
				issue_id, 
				platform,
				issue_title, 
				issue_subtitle, 
				app_version, 
				crash_count, 
				total_user, 
				event_timestamp, 
				issue_logs, 
				app_version_list, 
				last_update_timestamp
			)
		values
			(
				{issue_id},
				{platform},
				{issue_title},
				{issue_subtitle},
				{app_version},
				{crash_count},
				{total_user},
				{event_timestamp},
				{issue_logs}, 
				{app_version_list}, 
				{last_update_timestamp}
			)
		on duplicate key update	
			app_version = {app_version},
			platform = {platform},
			crash_count = {crash_count},
			total_user = {total_user},
			issue_logs = {issue_logs},
			app_version_list = {app_version_list},
			last_update_timestamp = {last_update_timestamp};	
	'''
	#IssueList = []
	for issue_id in issue_id_list:
		I=issues.Issue(issue_id=issue_id, table_index=table_index)
		try:
			#IssueList.append(I.modelize_issue())
			row = I.modelize_issue()

			insert_data_sql_cmd = INSERT_ISSUE_TO_DATABASE.format(
				table = table,
				issue_id = '"'+str(row['issue_id'])+'"',
				platform = '"'+str(row['platform'])+'"',
				issue_title = '"'+str(row['issue_title'])+'"',
				issue_subtitle = '"'+str(row['issue_subtitle'])+'"',
				# app version has ' " ' already
				app_version = str(row['app_version']),
				crash_count = '"'+str(row['crash_count'])+'"',
				total_user = '"'+str(row['total_user'])+'"',
				event_timestamp= '"'+str(row['event_timestamp'])+'"',
				issue_logs = '"'+str(row['issue_logs'])+'"',
				app_version_list= '"'+str(row['app_version_list'])+'"',
				last_update_timestamp= '"'+str(row['last_update_timestamp'])+'"'
			)

			#mydb.DBEngine.execute(insert_data_sql_cmd)
			#conn.execute(insert_data_sql_cmd)
			curs=mydb.execute(insert_data_sql_cmd)
			print('[sql_cmd]: ',insert_data_sql_cmd)
			print('>>> inserted item <<< ', curs.fetchone()['issue_logs'])
		except:
			print('[error on issue]: ',issue_id)
			print('[sql_cmd]: ',insert_data_sql_cmd)

	#print('Total issues: ', len(IssueList))

'''
##############################
#   API to userconfig class  #
##############################
'''
# DQS database info
userconfig_database = 'chinaqa'
userconfig_table = 'userconfig_config'

## local database info
#userconfig_database = 'qa'
#userconfig_table = 'userconfig_config'

acc_mode = 'rw'

def EmailMsg():
    msg = '<h1>Crash Monitor Retrieved </h1>'
    bookingValue = "<H3>Cron Job Completed !Check your crash lists</H3>"
    msg = msg + bookingValue
    return msg

def send_notification(**userconfig_notification):
	email_address = userconfig_notification['email_address']
	slack_channel = userconfig_notification['slack_channel']
	print("[Email Type] ",type(email_address))

	email = EmailHelper()
	title = 'Crash Monitor Notification'
	#email.booking_send_email("China.Quality@booking.com", email_address, title, EmailMsg() )
	if 'booking.com' in email_address:
		email.booking_send_email("Crash.Monitor@booking.com", email_address, title, EmailMsg() )
	
	if slack_channel is not None:
		email.booking_send_slack("Crash.Monitor",slack_channel, EmailMsg())

SELECT_EMAIL_SLACK_FROM_USERCONFIG_ID ='''
	SELECT 
		slack_channel,
		email_address
	FROM {userconfig_table}
	WHERE id={userconfig_id}
'''
def get_email_slack_from_userconfig_id(userconfig_id,userconfig_database=userconfig_database,userconfig_table=userconfig_table):
	mydb = dblib.DB(database=userconfig_database,acc_mode=acc_mode)
	select_email_slack_from_userconfig_id=SELECT_EMAIL_SLACK_FROM_USERCONFIG_ID.format(
							userconfig_table=userconfig_table,
							userconfig_id=userconfig_id	
	)

	curs=mydb.execute(select_email_slack_from_userconfig_id)
	return curs.fetchone()


def update_hit_issue_id_list_to_userconfig():
	CG = userconfig.ConfigGroup()
	# fetch all userconfig in 
	CG.get_userconfig_param()
	CG.get_configuser_issue_content_list()

	# all configuration in CG.configuser_list
	for configuser in CG.configuser_list:
		try:
			print(" [INFO] Retrieve Crash for team",configuser['team'],"###",configuser['id'])
			CU=userconfig.ConfigUser(**configuser)
			# step-1 filter all crashes based on crashcnt&totaluser from CrashIssueDbg
			CU.filter_issue_content_by_crashcnt_totaluser()
			CU.get_issue_with_files_and_keywords(write=True)

			userconfig_id = configuser['id']	
			userconfig_notification = get_email_slack_from_userconfig_id(userconfig_id)
			send_notification(**userconfig_notification)

		except Exception as e:
			print("[Exceptions] :",str(e))
			print(" >>> configuser content: ", configuser)	

#########################
#    Cron Jobs devops   #
#########################
def job_get_android_crash():
	print("start: job_get_android_crash \n")
	issue_id_list=get_crash_lists(table_index='android')
	print("done : get_crash_lists \n")
	write_issues_to_crashissue_database(issue_id_list=issue_id_list,acc_mode='rw',table_index='android')
	print("done :write_issues_to_crashissue_database \n")
	update_hit_issue_id_list_to_userconfig()
	# send notification

'''
def job_get_ios_crash():
	issue_id_list=get_crash_lists(table_index='android')
	write_issues_to_crashissue_database(issue_id_list=issue_id_list,acc_mode='rw',table_index='android')
	update_hit_issue_id_list_to_userconfig()
	# send notification
'''

def job_test():
	print('VarTime: ',start_timestamp_str)
	print('Now: ',datetime.utcnow())

if __name__ == '__main__':
	end_date =datetime.utcnow() 
	print('[job_get_android_crash] collect crash data within 7 days, end at : ', end_date)
	#schedule.every().day.at("03:30").do(job_get_android_crash)
	schedule.every(10).minutes.at(":20").do(job_get_android_crash)
	#print('[job_test]')
	#schedule.every(35).minutes.at(":20").do(job_test)


	while True:
		schedule.run_pending()
		time.sleep(1)
