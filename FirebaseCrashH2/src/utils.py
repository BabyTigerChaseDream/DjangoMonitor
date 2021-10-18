#/usr/local/bin/python3
#from FirebaseCrashH2.src.userconfig import CUser
import issues
import timelib 
import dblib
import firebase_db_common_lib 
from datetime import datetime, timedelta
import userconfig

import jsmod
import json
import os

#import schedule
import time

'''
#########################
#   API to Crash class  #
#########################
'''
#################################################################
# Configurable matrix: 
#################################################################
crash_count_max = '10'
total_user_max = '10'
issue_count_max = '20'

table_index = 'android'

# api for user input timing 
def setup_timeslot(end_date=datetime.utcnow(), delta=7):
	return timelib.timestamp().timeslot(end_date=end_date,delta=delta)

start_timestamp_str, end_timestamp_str = setup_timeslot(end_date=datetime.utcnow(), delta=7)

def get_crash_lists(table_index=table_index, start_timestamp_str=start_timestamp_str, end_timestamp_str=end_timestamp_str, 
								crash_count_max=crash_count_max, total_user_max=total_user_max, issue_count_max=issue_count_max):
	crashes = firebase_db_common_lib.Crashes(table_index=table_index, start_timestamp_str=start_timestamp_str, end_timestamp_str=end_timestamp_str, 
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

def write_issues_to_crashissue_database(issue_id_list, acc_mode, table='CrashIssuesBak', database='chinaqa'):
	#mydb = dblib.DB(database=database,acc_mode=acc_mode)
	mydb = dblib.DB(database=database,acc_mode=acc_mode)
	conn=mydb.connect()
	
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
			crash_count = {crash_count},
			total_user = {total_user},
			app_version_list = {app_version_list},
			last_update_timestamp = {last_update_timestamp};	
	'''
	#IssueList = []
	for issue_id in issue_id_list:
		I=issues.Issue(issue_id=issue_id)
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
			conn.execute(insert_data_sql_cmd)
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
#userconfig_database = 'chinaqa'
#userconfig_table = 'Config'

# local database info
userconfig_database = 'qa'
userconfig_table = 'userconfig_config'
userconfig_acc_mode = 'rw'

def write_to_cuser(conn, config_id, issue_id_list, table='userconfig'):
	issue_id_list_string =  ",".join(issue_id_list)
	UPDATE_ISSUE_ID_TO_DATABASE = '''
		update {table}
		set issue_id_list={issue_id_list}
		where id={config_id}
	'''
	try:
		sql_cmd = UPDATE_ISSUE_ID_TO_DATABASE.format(
			table = table,
			issue_id_list = '"'+str(issue_id_list_string)+'"',
			id = config_id
		)
		#mydb.DBEngine.execute(sql_cmd)
		conn.execute(sql_cmd)
	except:
			print('[error on issue]: ',config_id)
			print('[sql_cmd]: ',sql_cmd)

# comment out due to module missing 
#def write_issue_id_list_to_userconfig(acc_mode='rw', table='userconfig', database='qa'):
#	# DQS database info
#	#userconfig_database = 'chinaqa'
#	#userconfig_table = 'Config'
#
#	# local database info
#	userconfig_database = 'qa'
#	userconfig_table = 'userconfig_config'
#	userconfig_acc_mode = 'rw'
#	
#	mydb = dblib.DB(database=database,acc_mode=acc_mode)
#	conn=mydb.connect()
#
#	CGroup = userconfig.CGroup(database=userconfig_database, table=userconfig_table, acc_mode=userconfig_acc_mode)
#	# fetch all config in database
#	CGroup.fetchall()
#	CGroup.all_userconfig
#
#	for config in CGroup.all_userconfig:
#		CUser = userconfig.CUser(**config)
#		CUser.get_issue_with_files_and_keywords()
#		config_id =  CUser.id
#		issue_id_list = CUser.issue_with_files_and_keywords_list
#		write_to_cuser(conn=conn, config_id=config_id, issue_id_list=issue_id_list, table=table)	

#########################
# devops #
#########################
def job_get_crash():
	issue_id_list = get_crash_lists()
	dump_issues(issue_id_list)

def job_test():
	print('VarTime: ',start_timestamp_str)
	print('Now: ',datetime.utcnow())

'''
if __name__ == '__main__':
	end_date =datetime.utcnow() 
	delta = 7
	print('collect crash data within 7 days, end at : ', end_date)
	#schedule.every().day.at("06:00").do(job_get_crash)
	schedule.every().minute.at(":17").do(job_test)

	while True:
		schedule.run_pending()
		time.sleep(1)
'''
