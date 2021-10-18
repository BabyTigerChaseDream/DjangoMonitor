#/usr/local/bin/python3
import MySQLdb
import json 
import dblib

'''
db = MySQLdb.connect(host="localhost",
 	user='django',
 	password='123456',
 	db='qa')
 
cursor=db.cursor()
cursor.execute('show databases;')
# minor diff from bkng-lib
cursor.fetchall()
'''

conn = dblib.DB(simulate=False).connect()

# store Issue 
CREATE_TABLE_FOR_ISSUES = '''
	CREATE TABLE if not exists `CrashIssues` (
		`issue_id` varchar(255) NOT NULL,
		`platform` varchar(255) NOT NULL,
		`issue_title` varchar(500) DEFAULT NULL,
		`issue_subtitle` varchar(500) DEFAULT NULL,
		`app_version` varchar(255) DEFAULT NULL,
		`crash_count` int(10) unsigned NOT NULL DEFAULT '0',
		`total_user` int(10) unsigned NOT NULL DEFAULT '0',
		`event_timestamp` varchar(255) DEFAULT NULL,
		`issue_logs` text,
		`app_version_list` text,
		`last_update_timestamp` varchar(255) DEFAULT NULL,
		PRIMARY KEY (`issue_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;
'''

#cursor.execute(CREATE_TABLE_FOR_ISSUES)
#cursor.fetchall()

conn.execute(CREATE_TABLE_FOR_ISSUES)
conn.fetchall()

CREATE_TABLE_ENTRY = '''
	insert into CrashIssues 
		(
			issue_id, 
			platform,
			issue_title, 
			issue_subtitle, 
			app_version, 
			crash_count, 
			total_user, 
			event_timestamp, 
			issue_logs, 
			app_version_list, 
			last_update_timestamp
		)
	values
		(
			{issue_id},
			{platform},
			{issue_title},
			{issue_subtitle},
			{app_version},
			{crash_count},
			{total_user},
			{event_timestamp},
			{issue_logs}, 
			{app_version_list}, 
			{last_update_timestamp}
		);	
	'''

def write_json_to_mysql(jsonfile='/Users/jiaguo/workspace/crashmonitor-bot/FirebaseCrashH2/debugging/issues.json'):
	with open(jsonfile, 'r') as fd:
		mysql_rows = json.load(fd)
		for i,row in enumerate(mysql_rows):
			insert_data_sql_cmd = CREATE_TABLE_ENTRY.format(
				issue_id = '"'+str(row['issue_id'])+'"',
				platform = '"'+str(row['platform'])+'"',
				issue_title = '"'+str(row['issue_title'])+'"',
				issue_subtitle = '"'+str(row['issue_subtitle'])+'"',
				# app version has ' " ' already
				app_version = str(row['app_version']),
				crash_count = '"'+str(row['crash_count'])+'"',
				total_user = '"'+str(row['total_user'])+'"',
				event_timestamp= '"'+str(row['event_timestamp'])+'"',
				issue_logs = '"'+str(row['issue_logs'])+'"',
				app_version_list= '"'+str(row['app_version_list'])+'"',
				last_update_timestamp= '"'+str(row['last_update_timestamp'])+'"'
			)
			#cursor.execute(insert_data_sql_cmd)
			conn.execute(insert_data_sql_cmd)

