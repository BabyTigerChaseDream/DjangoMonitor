#/usr/local/bin/python3
import issues
import timelib 
import firebase_db_common_lib 
from datetime import datetime, timedelta
import jsmod

import json
import os

import schedule,time

'''
	api to retrieve data from firebase 
	- debugging 
	- glue logic 
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


def job_get_crash():
	issue_id_list = get_crash_lists()
	dump_issues(issue_id_list)

def job_test():
	print('VarTime: ',start_timestamp_str)
	print('Now: ',datetime.utcnow())

if __name__ == '__main__':
	end_date =datetime.utcnow() 
	delta = 7
	print('collect crash data within 7 days, end at : ', end_date)
	#schedule.every().day.at("06:00").do(job_get_crash)
	schedule.every().minute.at(":17").do(job_test)

	while True:
		schedule.run_pending()
		time.sleep(1)
