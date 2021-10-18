#/usr/local/bin/python3
#from FirebaseCrashH2.src.draft_all_lib import DBEngine
from collections import namedtuple
import json
import dblib
import timelib
from datetime import datetime 

#DBEngine = dblib.DB().DBEngine
conn = dblib.DB().conn
table_index = 'android'
table = dblib.firebase_crash_table[table_index]
database = 'android'

# local database used for debugging 

class Issue:
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

	#def __init__(self, issue_id, table=table, DBEngine=DBEngine):
	#def __init__(self, issue_id, table=table, conn=conn):
	def __init__(self, issue_id, table=table, database=database, simulate=False):
		#self.DBEngine = DBEngine
		self.conn = dblib.DB(simulate=simulate).connect()
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

		self.exceptions = None 
		self.frames = None

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

	def myattr(self):
	    return self.__dict__	

	def get_cursor(self,sql_cmd=None):
		sql_cmd_use_database = 'use '+str(self.database)
		if not sql_cmd:
			sql_cmd = self.sql_cmd
		try:
			self.cursor = self.conn.execute(sql_cmd_use_database)
			#self.cursor = self.DBEngine.execute(sql_cmd)
			self.cursor = self.conn.execute(sql_cmd)
		except:
			print('[ERROR] failed to get cursor from sql_cmd')

		return self.cursor

	def get_cursor_app_versions(self,sql_cmd_app_versions=None):
		if not sql_cmd_app_versions:
			sql_cmd_app_versions = self.sql_cmd_app_versions
		try:
			#self.cursor_app_versions = self.DBEngine.execute(sql_cmd_app_versions)
			self.cursor_app_versions = self.conn.execute(sql_cmd_app_versions)
		except:
			print('[ERROR] failed to get app versions from sql_cmd_app_versions')

		return self.cursor_app_versions	

	def modelize_issue(self, exception_key='exceptions', issue_id_key='issue_id', sql_cmd=None, sql_cmd_app_versions=None)->dict:
		self.get_cursor(sql_cmd=sql_cmd)
		issue_content = self.cursor.fetchone()

		if len(issue_content) == 0:
			print("[Warning] issue_content empty ")

		self.content['platform']=issue_content['platform'] 
		self.content['issue_title']=issue_content['issue_title'] 
		self.content['issue_subtitle']=issue_content['issue_subtitle'] 
		self.content['app_version']= issue_content['app_version'] 
		self.content['crash_count']=issue_content['crash_count'] 
		self.content['total_user']=issue_content['total_user'] 
		self.content['event_timestamp']= issue_content['event_timestamp'].strftime('%Y-%m-%d %H:%M:%S')

		try:
			issue_exceptions = issue_content[exception_key]
		except:
			KeyError("Missing exceptions in issue_id:",issue_content[issue_id_key])
	
		#print('[issue_content keys] ',issue_content.keys() )
		#type(issue_content[exception_key])
		#<class 'str'>

		# don't change the orders of lines below:
		# exceptions -> frames -> logs 
		self.exceptions = json.loads(issue_exceptions)[0]

		self.get_issue_frames()
		# the order matters 
		self.content['issue_logs'] = self.get_logs()

		# get app_version_list
		self.get_cursor_app_versions(sql_cmd_app_versions=sql_cmd_app_versions)
		app_version_string = self.cursor_app_versions.fetchone()['app_version_list'] # -> str 

		# logic of distinct app versions
		app_version_list =  json.loads(app_version_string)
		# app_version list with dup app version to set 
		app_version_set =  set(app_version_list)
		app_version_str = str(app_version_set).strip('{').strip('}')
		self.content['app_version_list'] = app_version_str 

		# issue last updated timestamp
		self.content['last_update_timestamp'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

		# dict of issues
		return self.content

	def dump_to_json(self):
		print('place holder')
		pass

	def get_issue_frames(self, frames_key='frames')->list:
		if not self.exceptions:
			ValueError('Please run \'modelize_issue\' to get exceptions')
		# list of dict-> failure stracktrace 
		self.frames=self.exceptions[frames_key]

		return self.frames

	def get_files_in_frame(self,frames=None)->set:
		self.files = set()

		if not frames:
			frames = self.frames

		for frame in frames:
			self.files.add(frame['file'])
		
		return self.files 

	def get_symbols_in_frame(self,frames=None)->set:
		self.symbols= set()

		if not frames:
			frames = self.frames

		for frame in frames:
			self.symbols.add(frame['symbol'])
		
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
			self.logs += frame['file'] + sep + frame['symbol'] + '\n'
		
		return self.logs
