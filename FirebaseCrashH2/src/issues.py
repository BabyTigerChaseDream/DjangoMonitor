#/usr/local/bin/python3
#from FirebaseCrashH2.src.draft_all_lib import DBEngine
from collections import namedtuple
import json
import dblib

DBEngine = dblib.DB().DBEngine
table_index = 'android'
table = dblib.firebase_crash_table[table_index]

class Issue:
	RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID ='''
		select 
			issue_id,
			issue_title,
			issue_subtitle,
			application->'$display_version' as app_version,
			count(distinct event_id) as crash_count, 
			count(distinct installation_uuid) as total_users,
			event_timestamp,
			exceptions
		from `{table}` 
		where issue_id='{issue_id}';
	''' 
	def __init__(self, issue_id, table=table, DBEngine=DBEngine):
		self.DBEngine = DBEngine
		# sql to get data per request
		self.table = table

		# fields in django models of Issue table
		self.contents = {
			'issue_id' : str(issue_id),
			'issue_title' :'blank-title', 
			'issue_subtitle' : 'sub-blank-title', 
			'app_version' : '00.00',
			'crash_count' : 0 ,
			'total_users' :  0 ,
			'event_timestamp' : None, 
			'logs' : 'NA' 
		}

		self.exceptions = None 
		self.frames = None

		self.files = set()
		self.symbols = set()

		self.sql_cmd = Issue.RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID.format(
				table = table,
				issue_id = str(issue_id)
			)

	def myattr(self):
	    return self.__dict__	

	def get_cursor(self,sql_cmd=None):
		if not sql_cmd:
			sql_cmd = self.sql_cmd
		self.cursor = self.DBEngine.execute(sql_cmd)
		return self.cursor
	
	def modelize_issue(self, exception_key='exceptions', issue_id_key='issue_id', sql_cmd=None)->dict:
		self.get_cursor(sql_cmd=sql_cmd)
		issue_content = self.cursor.fetchone()

		self.content['issue_title']=issue_content['issue_title'] 
		self.content['issue_subtitle']=issue_content['issue_subtitle'] 
		self.content['app_version']= issue_content['app_version'] 
		self.content['crash_count']=issue_content['crash_count'] 
		self.content['total_users']=issue_content['total_users'] 
		self.content['event_timestamp']= issue_content['event_timestamp']
		self.content['logs'] = self.get_logs()

		try:
			issue_exceptions = issue_content[exception_key]
		except:
			KeyError("Missing exceptions in issue_id:",issue_content[issue_id_key])
	
		#print('[issue_content keys] ',issue_content.keys() )
		#type(issue_content[exception_key])
		#<class 'str'>

		self.exceptions = json.loads(issue_exceptions)[0]

		# dict of issues
		return issue_content

	def dump_to_json(self):
		print('place holder')
		pass

	def get_issue_frames(self, frames_key='frames')->list:
		if not self.exceptions:
			ValueError('Please run \'get_issue_exceptions\' to get exceptions')
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

	def files_filter(self,target_file:set,files=set())->bool:
		if not files:
			files = self.files
		return files.intersection(target_file) 
	
	def symbols_filter(self,target_symbol:set,symbols=set())->bool:
		if not symbols:
			files = self.symbols
		return symbols.intersection(target_symbol) 

	def get_logs(self, frames=None)->str:
		self.logs = ''
		sep = '@'

		if not frames:
			frames = self.frames
		for frame in frames:
			self.logs += frame['file'] + sep + frame['symbol'] + '\n'
		
		return self.logs