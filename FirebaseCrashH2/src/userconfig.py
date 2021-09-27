#/usr/local/bin/python3

#########################################
# retreive userconfig in Config table  
# one userconfig enter maps to one UserConfig Class
#########################################
import dblib
import firebase_db_common_lib
import issues

import utils

import timelib
from datetime import datetime, timedelta

ISSUE_LIMIT = 50
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

'''
# all configurations in Config models
'''
class CGroup:
	# DQS database info
	#userconfig_database = 'chinaqa'
	#userconfig_table = 'Config'

	# local database info
	userconfig_database = 'qa'
	userconfig_table = 'userconfig_config'
	userconfig_acc_mode = 'rw'

	def __init__(self, database=userconfig_database, table=userconfig_table, acc_mode=userconfig_acc_mode):
		self.mydb = dblib.DB(database=database,acc_mode=acc_mode)
		self.table=table
		self.all_userconfig=[]	

	# reading userconfig from userconfig database directly -> generate sql_cmd
	def fetchall(self):
		GET_USERCONFIG_SQLCMD='''
			select 
				id,
				team,
				crash_count,
				total_user,
				platform,
				files,
				keywords,
				timeslot
			from `{table}` 
		'''
		get_userconfig_sqlcmd =  GET_USERCONFIG_SQLCMD.format(table=self.table)
		# retrieve data 
		cursor = self.mydb.DBEngine.execute(get_userconfig_sqlcmd)	

		for config in cursor.fetchall():
			self.all_userconfig.append(config)

		self.userconfig_count = len(self.all_userconfig)
		print('Total userconfig read: ',len(self.all_userconfig) )

'''
# Single configuration 
'''
class CUser:
	def __init__(self, **kwargs):

		self.id = kwargs['id']
		self.team = kwargs['team']
		self.crash_count = kwargs['crash_count']
		self.total_user = kwargs['total_user']
		self.platform = kwargs['platform']
		self.files = kwargs['files']
		self.keywords = kwargs['keywords']
		self.timeslot = kwargs['timeslot']
		# date 
		self.end_date = datetime.utcnow()
		self.start_date = (datetime.utcnow() - timedelta(days=int(self.timeslot)) )

		self.table = dblib.firebase_crash_table[self.platform]

		# issue id based on different filters
		self.issue_id_list=[]
		self.issue_id_keywords_list=[]
		self.issue_id_files_list=[]

		self.Crashes = None
		self.IssueWorker = None

	def sqlcmd_filter_with_crash_user(self, table=None, start_timestamp_str=None, end_timestamp_str=None,
			crash_count_max=None, total_user_max=None, issue_count_max=ISSUE_LIMIT):

		SQLCMD_FILTER_ISSUE_BY_CRASH_AND_USER_COUNT ='''
			select 
				issue_id, 
				count(distinct event_id) as crash_count, 
				count(distinct installation_uuid) as total_user 
			from `{table}` 
			where 
				event_timestamp >= '{start_timestamp_str}' and event_timestamp <= '{end_timestamp_str}'
			group by issue_id
			having crash_count > {crash_count_max} and total_user > {total_user_max} 
			order by total_user desc limit {issue_count_max};
		'''

		if not table:
			table=self.table
		if not start_timestamp_str:
			start_timestamp_str=self.start_date.strftime(DATE_FORMAT)
		if not end_timestamp_str:
			end_timestamp_str = self.end_date.strftime(DATE_FORMAT)
		if not crash_count_max:
			crash_count_max	= self.crash_count
		if not total_user_max:
			total_user_max	= self.total_user

		self.Crashes = firebase_db_common_lib.Crashes(table_index=self.platform, start_timestamp_str=start_timestamp_str, end_timestamp_str=end_timestamp_str, 
								crash_count_max=crash_count_max, total_user_max=total_user_max, issue_count_max=issue_count_max)

		self.sqlcmd_filter_issue_by_crash_and_user_count = SQLCMD_FILTER_ISSUE_BY_CRASH_AND_USER_COUNT.format(
				table = dblib.firebase_crash_table[table],
				start_timestamp_str=start_timestamp_str,
				end_timestamp_str = end_timestamp_str,
				crash_count_max = crash_count_max,
				total_user_max = total_user_max,
				issue_count_max = issue_count_max					
		)
	
	def get_crash_user_issue_id_list(self, table=None, start_timestamp_str=None, end_timestamp_str=None,
			crash_count_max=None, total_user_max=None, issue_count_max=ISSUE_LIMIT, write=True, local_database='qa',local_table='CrashIssues'):

		if not self.sqlcmd_filter_issue_by_crash_and_user_count:
			self.sqlcmd_filter_with_crash_user(table=table, start_timestamp_str=start_timestamp_str, end_timestamp_str=end_timestamp_str,
				crash_count_max=crash_count_max, total_user_max=total_user_max, issue_count_max=issue_count_max)

		# Make sure sql_cmd is re-written ,so we can get crashes based on userconfig 
		self.Crashes.sql_cmd = self.sqlcmd_filter_issue_by_crash_and_user_count

		self.issue_id_list =self.Crashes.get_issue_id_list()

		total_issues = len(self.issue_id_list)
		print('Total [',total_issues,'] issues for config ID:[',self.id,']')	

		if write:
			print('[Info] Write retrieved issue ID to {local_database}.{local_table}'.format(local_database=local_database, local_table=local_table))
			utils.write_issues_to_crashissue_database(issue_id_list=self.issue_id_list, acc_mode='rw', table=local_table, database=local_database)

	# Issue_id_list contains basic crashes user wants
	# filter it further in API below 
	
	def filter_issue_id_with_files(self, write=True, local_database='qa',local_table='CrashIssues'):
		target_file_set = set()
		for issue_id in self.issue_id_list:
			I = issues.Issue(issue_id=issue_id)
			I.modelize_issue()
			I.get_issue_frames()
			I.get_files_in_frame()

			for f in self.files.strip().split(','):
				target_file_set.add(f)
				print('[DBG] file set for {issue_id}:{target_file_set}'.format(issue_id=issue_id,target_file_set=target_file_set))

			if (I.files_filter(target_file_set=target_file_set)):
				self.issue_id_files_list.append(issue_id)

		if write:
			print('[Info] Write retrieved issue ID to {local_database}.{local_table}'.format(local_database=local_database, local_table=local_table))
			utils.write_issues_to_crashissue_database(issue_id_list=self.issue_id_files_list, acc_mode='rw', table=local_table, database=local_database)
		
	def filter_issue_id_with_keywords(self, write=True, local_database='qa',local_table='CrashIssues'):
		target_symbol_set = set()
		for issue_id in self.issue_id_list:
			I = issues.Issue(issue_id=issue_id)
			I.modelize_issue()
			I.get_issue_frames()
			I.get_symbols_in_frame()

			# TODO : need to debug it some -see how user input
			for f in self.keywords.strip().split(','):
				target_symbol_set.add(f)
				print('[DBG] file set for {issue_id}:{target_symbol_set}'.format(issue_id=issue_id,target_symbol_set=target_symbol_set))

			if (I.symbols_filter(target_symbol=target_symbol_set)):
				self.issue_id_keywords_list.append(issue_id)

		if write:
			print('[Info] Write retrieved issue ID to {local_database}.{local_table}'.format(local_database=local_database, local_table=local_table))
			utils.write_issues_to_crashissue_database(issue_id_list=self.issue_id_keywords_list, acc_mode='rw', table=local_table, database=local_database)

	def get_issue_with_both_files_and_keywords(self):
		return set(self.issue_id_files_list).intersection(set(self.issue_id_keywords_list))

	def get_issue_with_either_files_and_keywords(self):
		return set(self.issue_id_files_list).union(set(self.issue_id_keywords_list))