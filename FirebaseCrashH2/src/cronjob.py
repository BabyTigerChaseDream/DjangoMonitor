#/usr/local/bin/python3
import utils
from email_helper import EmailHelper
import time

from apscheduler.schedulers.background import BackgroundScheduler
import time
import pytz

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
	print('collect crash data within 7 days, end at : ', end_date)
	#schedule.every().hour.do(job_get_android_crash)
	schedule.every().hour.do(job_test)

	while True:
		schedule.run_pending()
		time.sleep(1)
