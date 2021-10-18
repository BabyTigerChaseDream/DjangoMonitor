#/usr/local/bin/python3

from bkng.infra.db.dbconnectionmanager import DBConnectionManager
'''
import MySQLdb
import MySQLdb.cursors
'''


# Database configuration 
#################################################################
# Configurable matrix: 
#################################################################
database = 'android' 
# access mode of database 
acc_mode = 'ro'

# Mapping table:
firebase_crash_table ={
    'android':'firebase_crashlytics_com_booking_ANDROID',
    'ios':'firebase_crashlytics_com_booking_BookingApp_IOS',
    'jira':'firebase_crashlytics_jira_sync',
    'sync':'firebase_crashlytics_com_booking_ANDROID_sync'
}

# access BPlatform database by default
class DB:
	def __init__(self,simulate=True,database=database,acc_mode=acc_mode,user=None,password=None):
		# param for db access
		self.database = database
		self.acc_mode = acc_mode
		self.user = user
		self.password = password

		# mode : simulation/bplatform
		self.simulate = simulate

		# to be fill in: conn/cursor 
		self.cm = None
		# replace DBEngine -> conn
		#self.DBEngine = None	
		self.conn = None

	def connect(self):
		# simulate on mock data on localhost
		if (self.simulate):
			pass 
		# comment out on BKS 
			'''
			db = MySQLdb.connect(host="localhost",
				user='django',
				password='123456',
				db='qa',cursorclass=MySQLdb.cursors.DictCursor)
			self.conn=db.cursor()			
			'''
		# simulate on mock data on localhost
		else:
			self.cm=DBConnectionManager()
			#self.DBEngine = self.cm.get_connection(self.database, self.acc_mode)
			self.conn= self.cm.get_connection(self.database, self.acc_mode)
			#self.cur = self.DBEngine
		return self.conn

	def execute(self, sql_cmd):
		if not self.conn:
			self.connect()
		return self.conn.execute(sql_cmd)
		
