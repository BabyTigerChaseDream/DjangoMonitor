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
from json.decoder import JSONDecodeError
from typing import NamedTuple
from bkng.infra.db.dbconnectionmanager import DBConnectionManager
from datetime import datetime, timedelta

# data format
import json
from collections import namedtuple 

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

start_datetime = (datetime.utcnow() - timedelta(days=10))
#end_datetime = datetime.utcnow()
end_datetime = (datetime.utcnow() - timedelta(days=12))

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
crash_count_max = '50'
total_users_max = '20'
issue_count_max = '20'
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
sql_cmd = None

def execute(sql_cmd):
    cursor = DBEngine.execute(sql_cmd)
    return cursor	
#################################################################
# filter issues we need 
#################################################################
def get_firebase_crashlytics_cursor(table_index=table_index, start_timestamp=start_timestamp, end_timestamp=end_timestamp, 
							crash_count_max=crash_count_max, total_users_max=total_users_max, issue_count_max=issue_count_max):
    # read only database connection 
    sql_cmd = TOP_ISSUE_BY_CRASH_AND_USER_COUNT.format(
		table = firebase_crash_table[table_index],
		start_timestamp=start_timestamp,
		end_timestamp = end_timestamp,
		crash_count_max = crash_count_max,
		total_users_max = total_users_max,
		issue_count_max = issue_count_max
	)

    print('[sql cmd]\t',sql_cmd)
    return execute(sql_cmd) 
#################################################################
# get issue_id list 
#################################################################
def get_issue_id_list(cursor):
	issue_id_list = []
	for crashunit in cursor.fetchall():
		issue_id_list.append[crashunit['issue_id']]

	total_issues = len(issue_id_list)
	print('Total issues today: ',total_issues)	
	return issue_id_list
'''
TBD : issue obj -> issue_id 
'''

#################################################################
# retrieve [issue] id and [issue.exceptions] details/contents
#################################################################
# this cmd retreive all crash counts since crash first occur, no time slot limitation
RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID ='''
	select 
		issue_id,
		count(distinct event_id) as crash_count, 
		count(distinct installation_uuid) as total_users,
		exceptions
	from `{table}` 
	where issue_id={issue_id};
''' 
def get_issue_content_cursor(issue_id, table_index=table_index):
    # read only database connection 
    sql_cmd = RETRIEVE_ISSUE_CONTENT_BY_ISSUE_ID.format(
		table = firebase_crash_table[table_index],
		issue_id = issue_id
	)

    print('[sql cmd]\t',sql_cmd)
    return execute(sql_cmd) 

# get single issue exception
# np<->dict 
# https://stackoverflow.com/questions/43921240/pythonic-way-to-convert-a-dictionary-into-namedtuple-or-another-hashable-dict-li

# JSON_CONTAINS(target, candidate[, path])
# https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains
# JSON_KEYS(json_doc[, path])
# https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-search


def get_issue_exceptions(cursor, exception_key='exceptions', issue_id_key='issue_id'):
	issue_content = cursor.fetchone()
	try:
		issue_exceptions = issue_content[exception_key]
	except:
		KeyError("Missing exceptions in issue_id:",issue_content[issue_id_key])
	
	print('[issue_content keys] ',issue_content.keys() )

	#type(issue_content['exceptions'])
	#<class 'str'>
	return issue_exceptions

#============================#
# structual exceptions 
#============================#

def issue_exceptions_to_dict(issue_exceptions:str)->dict:
	try:
		# single element list -> dict 
		issue_exceptions_dict = json.loads(issue_exceptions)[0]
	except:
		JSONDecodeError("Failed json.loads of issue_exceptions")	
	
	print('[issue_exceptions keys] ',issue_exceptions_dict.keys() )

	return issue_exceptions_dict

# directly store to DB
def issue_exceptions_to_ntp(issue_exceptions:str)->NamedTuple:
	try:
		# single element list -> dict 
		issue_exceptions_dict = json.loads(issue_exceptions)[0]
	except:
		JSONDecodeError("Failed json.loads of issue_exceptions")

	issue_exceptions_namedtuple=namedtuple('issue_exceptions_namedtuple',issue_exceptions_dict)

	issue_exp_ntp=issue_exceptions_namedtuple(**issue_exceptions_dict)
	
	print('[issue_exp_ntp fields] ',issue_exp_ntp._fields )
	
	return issue_exp_ntp

#============================#
# structual frames 
#============================

def get_issue_frames(issue_exp_ntp:namedtuple)->dict:
	# list[0] -> dict
	issue_frames=issue_exp_ntp.frames[0]

	return issue_frames	

def frame_parser(issue_frames:dict):
	file_set = set()
	symbol_set = set()

	for issue_f in issue_frames:
		file_set.add(issue_f['file'])
		symbol_set.add(issue_f['symbol'])

	return file_set,symbol_set

def file_filter(file_set:set,filename:str)->bool:
	return filename in file_set
	
def symbol_filter(symbol_set:set,symbol_name:str)->bool:
	for s in symbol_set:
		if symbol_name in s:
			return True
	return False 