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
  1) retrieve userconfig entry from UserConfig table
  2) combo sql_cmd from 1) => excluding keywords/filenames
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
		# userparams:raw params from user 
		self.userparams=[]	
		# configuser_list: parameters pass to ConfigUser (sql_cmd/keywords/files/blacklist)
		self.configuser_list=[]	

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
	def get_configuser_issue_content_list(self, crash_table=None):
		GET_USERCONFIG_CRASHISSUE_SQLCMD = '''
			select 
				issue_id, 
				platform,
				crash_count,
				total_user,	
				issue_logs,
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
				id = config['id']
				team = config['team']
				platform = config['platform']
				crash_count = config['crash_count']
				total_user = config['total_user']
				self.get_userconfig_crashissue_sqlcmd = GET_USERCONFIG_CRASHISSUE_SQLCMD.format(
																crash_table=crash_table,
																platform = platform,
																crash_count=crash_count,
																total_user=total_user
															)

				# TODO: replace with 'config in self.cursor.fetchall()' 
				configuser_dict = {
					'user_sqlcmd':self.get_userconfig_crashissue_sqlcmd,
					'id': id,
					'team':team,
					'platform':platform,
					'files':config['files'],
					'keywords':config['keywords'],
					'issue_id_blacklist':config['issue_id_blacklist']
				}

				self.configuser_list.append(configuser_dict)

			except Exception as e:
				print("[Exceptions] :",str(e))
				print(" >>> config content: ", config)				
				print(" >>> userconfig_crashissue_sqlcmd: ", self.get_userconfig_crashissue_sqlcmd)				
	
'''
# Single configuration 
1) filter issue_id from chinaqa.CrashIssues
2) filter files and keywords based on 1) 
3) generate final issue_id lists which is user wants , write it back to userConfig doc
'''
# CUser(**CG.configuser_list[0]) -> works right 
class ConfigUser:
	database = 'chinaqa'
	userconfig_table = 'userconfig_config'
	crash_table = 'CrashIssuesDbg'
	acc_mode = 'rw'

	SAVE_MATCH_ISSUE_ID_LIST_TO_USERCONFIG='''
		update {userconfig_table}
		set issue_id_list={match_issue_id_list}
		where id={config_id}
	'''
	def __init__(self, database=database, simulate=False, acc_mode=acc_mode, **kwargs):
		try:
			self.id = kwargs['id']
			self.team = kwargs['team']
			self.crash_count = kwargs['crash_count']
			self.total_user = kwargs['total_user']
			self.platform = kwargs['platform']
			self.files = kwargs['files']
			self.keywords = kwargs['keywords']
			self.issue_id_blacklist = kwargs['issue_id_blacklist']
			self.user_sqlcmd = kwargs['user_sqlcmd']
		except Exception as e:
			print("[Exceptions] :",str(e))

		# setup database conn		
		self.conn = dblib.DB(simulate=simulate,database=database,acc_mode=acc_mode).connect()
		# issue id based on different filters
		self.issue_content_list=[]
		self.issue_id_keywords_hit_list=[]
		self.issue_id_files_hit_list=[]

		self.Crashes = None
		self.IssueWorker = None

		# cmd 
		self.sqlcmd_filter_issue_by_crash_and_user_count = None
		self.curvenow = None
	
	def get_cursor(self,user_sqlcmd):
		sql_cmd_use_database = 'use '+str(self.database)
		try:
			# first select the right database 
			self.cursor = self.conn.execute(sql_cmd_use_database)
			# then read data from table 
			self.cursor = self.conn.execute(user_sqlcmd)
		except Exception as e:
			print("[Exceptions] :",str(e))
			print("[user_sqlcmd] :",user_sqlcmd)

		return self.cursor

	def filter_issue_content_by_crashcnt_totaluser(self,user_sqlcmd=None):
		# fetch data in chinaqa.CrashIssues
		# return issue id list
		# Issue_id_list contains basic crashes user wants
		if not user_sqlcmd:
			user_sqlcmd = self.user_sqlcmd
		
		self.curvenow = self.get_cursor(user_sqlcmd=self.user_sqlcmd)
		self.issue_content_list = self.curvenow.fetchall() 
		return self.issue_content_list 
	
	def filter_issue_id_with_files(self,user_sqlcmd=None,write=False):
		if not self.issue_content_list:
			if not user_sqlcmd:
				user_sqlcmd = self.user_sqlcmd		
			try:
				self.filter_issue_content_by_crashcnt_totaluser(user_sqlcmd)
			except Exception as e:
				print("[Exceptions] :",str(e))			
				print(">>> self.issue_content_list: ",self.issue_content_list)
				print(">>> user_sqlcmd: ",user_sqlcmd)

		# clean state
		self.issue_id_files_list=[]
		#target_file_set = set()
		for issue_content in self.issue_content_list:
			try:
				issue_logs=issue_content['issue_logs']		
			except Exception as e:
				print("[Exceptions] :",str(e))			
				print(">>> user_sqlcmd:",issue_content)			

			for f in self.files.replace(' ','').split(','):
				if str(f) in issue_logs:
					self.issue_id_files_hit_list.append(issue_content['issue_id'])
		
		match_issue_id_list = "".join([i for i in self.issue_id_files_hit_list])
		print(match_issue_id_list)

		if write:
			print('[Info] Write retrieved issue ID to Userconfig table->issue_id_list')
			self.save_match_issue_id_list_to_userconfig = self.SAVE_MATCH_ISSUE_ID_LIST_TO_USERCONFIG.format(
					userconfig_table = self.userconfig_table,
					config_id= self.id,
					match_issue_id_list=match_issue_id_list,
			)
			self.get_cursor(self.save_match_issue_id_list_to_userconfig)
	'''
	
	def filter_issue_id_with_keywords(self, write=False, local_database='qa',local_table='CrashIssues'):
		# same as the func above 
		self.issue_id_keywords_hit_list = []

	def get_issue_with_files_and_keywords(self)->list:
		if not self.issue_id_keywords_list:
			self.filter_issue_id_with_keywords()
		if not self.issue_id_files_list:
			self.filter_issue_id_with_files()
		
		self.issue_with_files_and_keywords_list = list( 
			set(self.issue_id_files_list).intersection(set(self.issue_id_keywords_list)) 
			)
		
		return self.issue_with_files_and_keywords_list 

	def writeback_issue_id_list_to_userconfig(self):
		pass

	'''	