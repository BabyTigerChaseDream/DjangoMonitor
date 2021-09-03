#/usr/local/bin/python3

#########################################
# retreive firebase database crash data #
#########################################
# parameter : time range; user affected; crash count per issue_id
import dblib
import timelib

from datetime import datetime, timedelta
# data format
import json

#################################################################
# Configurable matrix: 
#################################################################
crash_count_max = '10'
total_users_max = '10'
issue_count_max = '20'

table_index = 'android'

############################
# TBD: replace with timelib 
############################
'''
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

end_datetime = (datetime.utcnow() - timedelta(days=10))
start_datetime = (datetime.utcnow() - timedelta(days=12))

start_timestamp = start_datetime.strftime(DATE_FORMAT)
end_timestamp = end_datetime.strftime(DATE_FORMAT)
'''

start_timestamp, end_timestamp = timelib.timestamp().timeslot()

############################

class Crashes:
	# sql to get data per request
	TOP_ISSUE_BY_CRASH_AND_USER_COUNT ='''
		select 
			issue_id, 
			application->'$.display_version' as app_version, 
			count(distinct event_id) as crash_count, 
			count(distinct installation_uuid) as total_users 
		from `{table}` 
		where 
			event_timestamp >= '{start_timestamp}' and event_timestamp <= '{end_timestamp}'
		group by issue_id
		having crash_count > {crash_count_max} and total_users > {total_users_max} 
		order by total_users desc limit {issue_count_max};
	''' 
	def __init__(self, table_index=table_index, start_timestamp=start_timestamp, end_timestamp=end_timestamp, 
								crash_count_max=crash_count_max, total_users_max=total_users_max, issue_count_max=issue_count_max):

		DBEngine = dblib.DB().DBEngine
		try:
	    # read only database connection 
			self.sql_cmd = self.TOP_ISSUE_BY_CRASH_AND_USER_COUNT.format(
				table = dblib.firebase_crash_table[table_index],
				start_timestamp=start_timestamp,
				end_timestamp = end_timestamp,
				crash_count_max = crash_count_max,
				total_users_max = total_users_max,
				issue_count_max = issue_count_max
			)
		except:
			ValueError("[sql_cmd] ",self.sql_cmd)

		self.DBEngine = DBEngine

	def get_cursor(self,sql_cmd=None):
		if not sql_cmd:
			sql_cmd = self.sql_cmd
		self.cursor = self.DBEngine.execute(sql_cmd)
		return self.cursor
		
	##########################
	# get issue_id list 
	##########################
	def get_issue_id_list(self, issue_id_key='issue_id'):
		issue_id_list = []
		for crash in self.cursor.fetchall():
			issue_id_list.append[crash[issue_id_key]]

		total_issues = len(issue_id_list)
		print('Total issues today: ',total_issues)	
		return issue_id_list