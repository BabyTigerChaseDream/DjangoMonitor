#/usr/local/bin/python3
#from FirebaseCrashH2.src.draft_all_lib import DBEngine
from collections import namedtuple
import json

from sqlalchemy.util.langhelpers import symbol
import dblib
import timelib
from datetime import datetime 

import firebase_db_common_lib


#DBEngine = dblib.DB().DBEngine
conn = dblib.DB().conn
#DB name
database = 'android'


# local database used for debugging 

class Issue:
	### issue for a specific uuid 
	RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID ='''
		select 
			issue_id,
			platform,
			issue_title,
			issue_subtitle,
			application->'$.display_version' as app_version,
			count(distinct event_id) as crash_count, 
			count(distinct installation_uuid) as total_user,
			event_timestamp,
			exceptions
		from `{table}` 
		where issue_id='{issue_id}';
	''' 

	RETRIEVE_ISSUE_APP_VERSIONS_BY_ISSUE_ID = '''
		select 
			issue_id, 
			JSON_ARRAYAGG(application->'$.display_version') as app_version_list
		from `{table}` 
		where issue_id='{issue_id}';
	'''
	### collect issue data per time slot
	### we still need table : firebase_crash_table

	COLLECT_ISSUE_BY_CRASH_AND_USER_COUNT_PER_TIMESLOT ='''
		select 
			application->'$.display_version' as app_version, 
			count(distinct event_id) as crash_count, 
			count(distinct installation_uuid) as total_user 
		from `{table}` 
		where 
			event_timestamp >= '{start_timestamp_str}' and event_timestamp <= '{end_timestamp_str}' and issue_id='{issue_id}'
	''' 

	RETRIEVE_STACKTRACES_BY_ISSUE_ID = '''
		select 
			stacktraces 
		from `{stacktrace_table}` 
		where issue_id='{issue_id}' order by insert_id desc limit 1;
	'''

	stacktrace_table = 'firebase_crashlytics_stacktraces'
	start_timestamp_str =firebase_db_common_lib.start_timestamp_str
	end_timestamp_str =firebase_db_common_lib.end_timestamp_str 

	def __init__(self, issue_id, table_index, database=database, simulate=False):
		# tables in database above
		# table_index ='android' / 'iOS'	
		self.table_index = table_index
		table = dblib.firebase_crash_table[table_index]

		#self.DBEngine = DBEngine
		self.conn = dblib.DB(simulate=simulate).connect()
		self.issue_id = str(issue_id)
		# specify both database and table , in order to access right
		self.table = table
		self.database = database 

		# fields in django models of Issue table
		self.content = {
			'issue_id' : str(issue_id),
			'platform' : 'mobile',
			'issue_title' :'blank-title', 
			'issue_subtitle' : 'sub-blank-title', 
			'app_version' : '0',
			'crash_count' : 0 ,
			'total_user' :  0 ,
			# timestamp to string 
			'event_timestamp' : 'now', 
			'issue_logs' : 'NA',
			'app_version_list':'00.00',
			'last_update_timestamp' : 'now'	
		}

		self.frames = None
		self.stacktraces= None

		self.files = set()
		self.symbols = set()

		self.sql_cmd = Issue.RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID.format(
				table = table,
				issue_id = str(issue_id)
			)

		self.sql_cmd_app_versions = Issue.RETRIEVE_ISSUE_APP_VERSIONS_BY_ISSUE_ID.format(
				table = table,
				issue_id = str(issue_id)
			)

		self.sql_cmd_stacktraces = Issue.RETRIEVE_STACKTRACES_BY_ISSUE_ID.format(
			stacktrace_table=self.stacktrace_table,
			issue_id = issue_id 
		)
	def myattr(self):
	    return self.__dict__	

	def get_cursor(self,sql_cmd=None):
		sql_cmd_use_database = 'use '+str(self.database)
		if not sql_cmd:
			sql_cmd = self.sql_cmd
		try:
			# first select the right database 
			self.cursor = self.conn.execute(sql_cmd_use_database)
			# then read data from table 
			self.cursor = self.conn.execute(sql_cmd)
		except:
			print('[ERROR] failed to get cursor from sql_cmd')

		return self.cursor
	
	def get_timeslot_static_data(self,start_timestamp_str=None, end_timestamp_str=None):
		if not start_timestamp_str:
			start_timestamp_str=self.start_timestamp_str

		if not end_timestamp_str:
			end_timestamp_str=self.end_timestamp_str

		self.collect_issue_by_crash_and_user_count_per_timeslot = self.COLLECT_ISSUE_BY_CRASH_AND_USER_COUNT_PER_TIMESLOT.format(
				table = self.table,
				start_timestamp_str=start_timestamp_str,
				end_timestamp_str = end_timestamp_str,
				issue_id = self.issue_id
			)
		print("[get_timeslot_static_data sql_cmd] \
				", self.collect_issue_by_crash_and_user_count_per_timeslot)

		self.get_cursor(self.collect_issue_by_crash_and_user_count_per_timeslot)

		self.issue_static_data = self.cursor.fetchone()
		return self.issue_static_data 

		

	def get_cursor_app_versions(self,sql_cmd_app_versions=None):
		if not sql_cmd_app_versions:
			sql_cmd_app_versions = self.sql_cmd_app_versions
		try:
			#self.cursor_app_versions = self.DBEngine.execute(sql_cmd_app_versions)
			self.cursor_app_versions = self.conn.execute(sql_cmd_app_versions)
		except:
			print('[ERROR] failed to get app versions from sql_cmd_app_versions')

		return self.cursor_app_versions	

	def modelize_issue(self, sql_cmd=None, sql_cmd_app_versions=None)->dict:
		#[notes] one time only
		self.get_cursor(sql_cmd=sql_cmd)
		issue_content = self.cursor.fetchone()

		if len(issue_content) == 0:
			print("[Warning] issue_content empty ")

		try:
			# comment out 'platform' since firebase reassign it to null, use table_index -> platform
			#self.content['platform']=issue_content['platform'] 
			self.content['platform']= self.table_index
			self.content['issue_title']=issue_content['issue_title'] 
			self.content['issue_subtitle']=issue_content['issue_subtitle'] 
			self.content['app_version']= issue_content['app_version'] 
			self.content['crash_count']=issue_content['crash_count'] 
			self.content['total_user']=issue_content['total_user'] 
			self.content['event_timestamp']= issue_content['event_timestamp'].strftime('%Y-%m-%d %H:%M:%S')

			self.get_issue_frames()
			# the order matters 
			self.content['issue_logs'] = self.get_logs()

		except Exception as e:
			print("[Exceptions] :",str(e))
			print(" >>> issue_content :\n",)
			for k,v in issue_content.items():
				print("{k}:{v}".format(k=k,v=v) )

		# get app_version_list
		self.get_cursor_app_versions(sql_cmd_app_versions=sql_cmd_app_versions)
		app_version_string = self.cursor_app_versions.fetchone()['app_version_list'] # -> str 

		# logic of distinct app versions
		app_version_list =  json.loads(app_version_string)
		# app_version list with dup app version to set 
		app_version_set =  set(app_version_list)
		app_version_str = str(app_version_set).strip('{').strip('}')
		self.content['app_version_list'] = app_version_str 

		# get crash count / total user
		static_data = self.get_timeslot_static_data()
		self.content['crash_count']=static_data['crash_count'] 
		self.content['total_user']=static_data['total_user'] 	
		self.content['app_version']=static_data['app_version'] 	

		# issue last updated timestamp
		self.content['last_update_timestamp'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

		# dict of issues
		return self.content

	def dump_to_json(self):
		print('place holder')
		pass

	def get_stacktraces(self)->list:
		self.get_cursor(sql_cmd=self.sql_cmd_stacktraces)
		try:
			stacktraces=self.cursor.fetchone()
			self.stacktraces = json.loads(stacktraces['stacktraces'])
		except Exception as e:
			print("[Exceptions] :",str(e))		
		
		return self.stacktraces

	def get_issue_frames(self)->list:
		if not self.stacktraces:
			try:
				self.get_stacktraces()
				frames = []
				# first get subtitle,title,exception messages as a whole 
				frames.extend(s['title'] for s in self.stacktraces)
				frames.extend(s['subtitle'] for s in self.stacktraces)
				frames.extend(s['exception_message'] for s in self.stacktraces)
				# add issue frames 
				frames.extend(s['frames'] for s in self.stacktraces)
				self.frames = frames[0]
			except Exception as e:
				print("[Exceptions] :",str(e))		
				print("	>>> stacktraces content <<<",self.stacktraces)
		
		return self.frames

	def get_files_in_frame(self)->set:
		self.files = set()

		if not self.frames:
			frames = self.get_issue_frames()

		for frame in frames:
			try:
				file_name = frame['file'] or 'NA'
				self.files.add(file_name)
			
			except Exception as e:
				print("[Exceptions] :",str(e))	
		return self.files 

	def get_symbols_in_frame(self,frames=None)->set:
		self.symbols= set()

		if not frames:
			frames = self.frames

		for frame in frames:
			symbol_name = frame['symbol'] or 'NA'
			self.symbols.add(symbol_name)
		
		return self.symbols 

	def files_filter(self,target_file_set:set,files=set())->bool:
		if not files:
			files = self.files
		return files.intersection(target_file_set) 
	
	def symbols_filter(self,target_symbol_set:set,symbols=set())->bool:
		if not symbols:
			files = self.symbols
		return symbols.intersection(target_symbol_set) 

	def get_logs(self, frames=None)->str:
		self.logs = ''
		sep = '@'

		if not frames:
			frames = self.frames
		for frame in frames:
			file_name = frame['file'] or 'NA' 
			symbol_name = frame['symbol'] or 'NA'	
			self.logs += file_name + sep + symbol_name + '\n'
		
		return self.logs
