#/usr/local/bin/python3

#########################################
# retreive firebase database crash data #
#########################################
# parameter : time range; user affected; crash count per issue_id
'''
# User 3rd party lib : 'bkng-infra-libs' : 
# directly retrieve data on kvm crash database 
--------------------------------------------------------------------  
Guide to install Booking infra database lib: 
	https://gitlab.booking.com/python/bkng/-/tree/master/infra/db
'''
#import requests
from bkng.infra.db.dbconnectionmanager import DBConnectionManager
from datetime import datetime, timedelta

# data format
import json
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

start_datetime = (datetime.utcnow() - timedelta(days=1))
end_datetime = datetime.utcnow()

start_timestamp = start_datetime.strftime(DATE_FORMAT)
end_timestamp = end_datetime.strftime(DATE_FORMAT)

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
table_index = 'android'

##### crash filter 
crash_count_max = '150'
total_users_max = '50'
issue_count_max = '45'
#################################################################
# setup DBConnections
#################################################################

def init():
	cm=DBConnectionManager()
	DBEngine = cm.get_connection(database, acc_mode)
	return cm, DBEngine

cm,DBEngine = init()

#################################################################
# Common Lib DBConnections
#################################################################
# sql to get data per request
TOP_ISSUE_BY_CRASH_AND_USER_COUNT ='''
	select 
		issue_id, 
		application->'$.display_version' as app_version, 
		count(distinct event_id) as crash_count, 
		count(distinct installation_uuid) as total_users 
	from `{table}` 
	where 
		event_timestamp >= '{start_timestamp}' and event_timestamp <= '{end_timestamp}'
	group by issue_id
	having crash_count > {crash_count_max} and total_users > {total_users_max} 
	order by total_users desc limit {issue_count_max};
''' 

def execute(sql_cmd=sql_cmd):
    cursor = DBEngine.execute(sql_cmd)
    return cursor	

def get_firebase_crashlytics_cursor(index=table_index):
    # read only database connection 
    sql_cmd = TOP_ISSUE_BY_CRASH_AND_USER_COUNT.format(
		table = firebase_crash_table[index],
		start_timestamp=start_timestamp,
		end_timestamp = end_timestamp,
		crash_count_max = crash_count_max,
		total_users_max = total_users_max,
		issue_count_max = issue_count_max
	)

    cursor = DBEngine.execute(sql_cmd)
    return cursor

# TODO : get issue_id from read_firebase_crashlytics & call https API to get failing details 

def get_issue_id_list(cursor):
	issue_id_list = []
	for issue_id in cursor.fetchall():
		issue_id_list.append[issue_id]

	total_issues = len(issue_id_list)
	print('Total issues today: ',total_issues)	
	return issue_id_list
