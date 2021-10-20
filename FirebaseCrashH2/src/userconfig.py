#/usr/local/bin/python3

#########################################
# retreive userconfig in Config table  
# one userconfig enter maps to one UserConfig Class
#########################################
from sys import platform
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
class ConfigGroup:
	# local database info
	database = 'chinaqa'
	userconfig_table = 'userconfig_config'
	crash_table = 'CrashIssuesDbg'
	acc_mode = 'rw'

	def __init__(self, database=database, userconfig_table=userconfig_table, 
				acc_mode=acc_mode):
		self.mydb = dblib.DB(database=database,acc_mode=acc_mode,simulate=False)
		self.conn = self.mydb.connect()
		self.userconfig_table=userconfig_table
		self.userparams=[]	
		self.user_sqlcmd=[]	

	# reading userconfig parameters from userconfig database 
	def get_userconfig_param(self):
		GET_USERCONFIG_PARAM_SQLCMD='''
			select 
				id, 
				team,
				platform,
				crash_count,
				total_user,
				files,
				keywords,
				issue_id_blacklist
			from `{userconfig_table}`
		'''
		self.get_userconfig_param_sqlcmd = GET_USERCONFIG_PARAM_SQLCMD.format(userconfig_table=self.userconfig_table)
		try:
			self.cursor = self.conn.execute(self.get_userconfig_param_sqlcmd)

		except Exception as e:
			print("[Exceptions] :",str(e))
			print(" >>> userconfig_param_sqlcmd:\n\t ",
					self.get_userconfig_param_sqlcmd)

		for config in self.cursor.fetchall():
			self.userparams.append(config)

		self.userconfig_count = len(self.userparams)
		print('Total userconfig read: ',len(self.userparams) )

	# generate sql_cmd from 'get_userconfig_param' 
	def get_userconfig_sqlcmd(self, crash_table=None):
		GET_USERCONFIG_CRASHISSUE_SQLCMD = '''
			select 
				issue_id, 
				platform,
				crash_count,
				total_user,	
			from `{crash_table}` 
			where 
				platform = '{platform}' and crash_count >= '{crash_count}' and total_user >= '{total_user}'
			order by total_user desc;
		''' 
		# TODO : version to check black_list
		if crash_table is None:
			crash_table = self.crash_table

		# iterate all userconfig parameters:
		for config in self.userparams:
			try:
				platform = config['platform']
				crash_count = config['crash_count']
				total_user = config['total_user']
				self.get_userconfig_crashissue_sqlcmd = GET_USERCONFIG_CRASHISSUE_SQLCMD.format(
																crash_table=crash_table,
																platform = platform,
																crash_count=crash_count,
																total_user=total_user
																)
				self.user_sqlcmd.append(self.get_userconfig_crashissue_sqlcmd)
			except Exception as e:
				print("[Exceptions] :",str(e))
				print(" >>> config content: ", config)				
				print(" >>> userconfig_crashissue_sqlcmd: ", self.get_userconfig_crashissue_sqlcmd)				


'''
# Single configuration 
'''
# CUser(**CG.all_userconfig[0]) -> works right 
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

		# cmd 
		self.sqlcmd_filter_issue_by_crash_and_user_count = None

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

		self.sqlcmd_filter_issue_by_crash_and_user_count_raw = SQLCMD_FILTER_ISSUE_BY_CRASH_AND_USER_COUNT.format(
				table = self.table,
				start_timestamp_str=start_timestamp_str,
				end_timestamp_str = end_timestamp_str,
				crash_count_max = crash_count_max,
				total_user_max = total_user_max,
				issue_count_max = issue_count_max					
		)
		self.sqlcmd_filter_issue_by_crash_and_user_count = self.sqlcmd_filter_issue_by_crash_and_user_count_raw.replace('\t',' ').replace('\n',' ')
		return self.sqlcmd_filter_issue_by_crash_and_user_count
	
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
	
	def filter_issue_id_with_files(self, write=False, local_database='qa',local_table='CrashIssues'):
		target_file_set = set()

		if not self.issue_id_list:
			self.get_crash_user_issue_id_list()

		for issue_id in self.issue_id_list:
			I = issues.Issue(issue_id=issue_id)
			I.modelize_issue()
			I.get_issue_frames()
			I.get_files_in_frame()

			for f in self.files.replace(' ','').split(','):
				target_file_set.add(f)
				print('[DBG] file set for {issue_id}:{target_file_set}'.format(issue_id=issue_id,target_file_set=target_file_set))

			if (I.files_filter(target_file_set=target_file_set)):
				self.issue_id_files_list.append(issue_id)

		if write:
			print('[Info] Write retrieved issue ID to {local_database}.{local_table}'.format(local_database=local_database, local_table=local_table))
			utils.write_issues_to_crashissue_database(issue_id_list=self.issue_id_files_list, acc_mode='rw', table=local_table, database=local_database)
		
	def filter_issue_id_with_keywords(self, write=False, local_database='qa',local_table='CrashIssues'):
		target_symbol_set = set()

		if not self.issue_id_list:
			self.get_crash_user_issue_id_list()

		for issue_id in self.issue_id_list:
			I = issues.Issue(issue_id=issue_id)
			I.modelize_issue()
			I.get_issue_frames()
			I.get_symbols_in_frame()

			# TODO : need to debug it some -see how user input
			for f in self.keywords.replace(' ','').split(','):
				target_symbol_set.add(f)
				print('[DBG] file set for {issue_id}:{target_symbol_set}'.format(issue_id=issue_id,target_symbol_set=target_symbol_set))

			if (I.symbols_filter(target_symbol=target_symbol_set)):
				self.issue_id_keywords_list.append(issue_id)

		if write:
			print('[Info] Write retrieved issue ID to {local_database}.{local_table}'.format(local_database=local_database, local_table=local_table))
			utils.write_issues_to_crashissue_database(issue_id_list=self.issue_id_keywords_list, acc_mode='rw', table=local_table, database=local_database)

	def get_issue_with_files_and_keywords(self)->list:
		if not self.issue_id_keywords_list:
			self.filter_issue_id_with_keywords()
		if not self.issue_id_files_list:
			self.filter_issue_id_with_files()
		
		self.issue_with_files_and_keywords_list = list( 
			set(self.issue_id_files_list).intersection(set(self.issue_id_keywords_list)) 
			)
		
		return self.issue_with_files_and_keywords_list 
	'''
	def get_issue_with_files_or_keywords(self)->list:
		if not self.issue_id_keywords_list:
			self.filter_issue_id_with_keywords()
		if not self.issue_id_files_list:
			self.filter_issue_id_with_files()

		self.issue_with_files_or_keywords_list = list( 
			set(self.issue_id_files_list).union(set(self.issue_id_keywords_list)) 
			)
		return self.issue_with_files_or_keywords_list 
	'''