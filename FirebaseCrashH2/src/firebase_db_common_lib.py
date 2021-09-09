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

import sys
#################################################################
# Configurable matrix: 
#################################################################
crash_count_max = '10'
total_users_max = '10'
issue_count_max = '20'

table_index = 'android'

############################
# timelib 
############################

start_timestamp_str, end_timestamp_str = timelib.timestamp().timeslot()

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
			event_timestamp >= '{start_timestamp_str}' and event_timestamp <= '{end_timestamp_str}'
		group by issue_id
		having crash_count > {crash_count_max} and total_users > {total_users_max} 
		order by total_users desc limit {issue_count_max};
	''' 
	def __init__(self, table_index=table_index, start_timestamp_str=start_timestamp_str, end_timestamp_str=end_timestamp_str, 
								crash_count_max=crash_count_max, total_users_max=total_users_max, issue_count_max=issue_count_max):

		DBEngine = dblib.DB().DBEngine
		self.issue_id_list = []
		try:
	    # read only database connection 
			self.sql_cmd = self.TOP_ISSUE_BY_CRASH_AND_USER_COUNT.format(
				table = dblib.firebase_crash_table[table_index],
				start_timestamp_str=start_timestamp_str,
				end_timestamp_str = end_timestamp_str,
				crash_count_max = crash_count_max,
				total_users_max = total_users_max,
				issue_count_max = issue_count_max
			)
		except ValueError:
			print("[sql_cmd] ",self.sql_cmd)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise

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
		# in case cursor is empty - can be dumped once only, need to re-read cursor
		print('[Init] dump cursor: ',self.sql_cmd)
		self.cursor = self.get_cursor()

		try:
			for crash in self.cursor.fetchall():
				print(crash)
				self.issue_id_list.append(crash[issue_id_key])
		except AttributeError:
			print('missing attribute : ',issue_id_key)
		except:
			print("Unexpected error:", sys.exc_info()[0])
			raise


		total_issues = len(self.issue_id_list)
		print('Total issues today: ',total_issues)	
		return self.issue_id_list