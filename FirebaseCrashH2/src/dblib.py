#/usr/local/bin/python3

from bkng.infra.db.dbconnectionmanager import DBConnectionManager

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

class DB:
	def __init__(self,database=database,acc_mode=acc_mode):
		#self.cm = None
		#self.DBEngine = None

		cm=DBConnectionManager()
		DBEngine = cm.get_connection(database, acc_mode)

		self.cm=cm
		self.DBEngine = DBEngine
		#return self.DBEngine
