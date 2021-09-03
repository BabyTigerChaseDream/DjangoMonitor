#/usr/local/bin/python3
from bkng.infra.db.dbconnectionmanager import DBConnectionManager
from collections import namedtuple
import json

database = 'android' 
acc_mode = 'ro'

class DB:
	def __init__(self,database=database,acc_mode=acc_mode):
		#self.cm = None
		#self.DBEngine = None

		cm=DBConnectionManager()
		DBEngine = cm.get_connection(database, acc_mode)

		self.cm=cm
		self.DBEngine = DBEngine
		#return self.DBEngine

class Issue:
	RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID ='''
		select 
			issue_id,
			count(distinct event_id) as crash_count, 
			count(distinct installation_uuid) as total_users,
			exceptions
		from `{table}` 
		where issue_id='{issue_id}';
	''' 
	def __init__(self, issue_id, table='firebase_crashlytics_com_booking_ANDROID', DBEngine=None):
		self.DBEngine = DB().DBEngine
		# sql to get data per request
		self.table = table
		self.issue_id = str(issue_id)
		
		self.exceptions = None 
		self.frames = None 

		self.files = set()
		self.symbols = set()

		self.sql_cmd = Issue.RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID.format(
				table = table,
				issue_id = str(issue_id)
			)

	def get_issue(self,sql_cmd=None):
		if not sql_cmd:
			sql_cmd = self.sql_cmd
		self.cursor = self.DBEngine.execute(sql_cmd)
		return self.cursor
	
	def get_issue_exceptions(self, exception_key='exceptions', issue_id_key='issue_id')->dict:
		issue_content = self.cursor.fetchone()
		try:
			issue_exceptions = issue_content[exception_key]
		except:
			KeyError("Missing exceptions in issue_id:",issue_content[issue_id_key])
	
		#print('[issue_content keys] ',issue_content.keys() )
		#type(issue_content['exceptions'])
		#<class 'str'>

		self.exceptions = json.loads(issue_exceptions)[0]
		return self.exceptions

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
			self.symbols.add(frame['symbols'])
		
		return self.symbols 

	def files_filter(self,target_file:set,files=set())->bool:
		if not files:
			files = self.files
		return files.intersection(target_file) 
	
	def symbols_filter(self,target_symbol:set,symbols=set())->bool:
		if not symbols:
			files = self.symbols
		return symbols.intersection(target_symbol) 