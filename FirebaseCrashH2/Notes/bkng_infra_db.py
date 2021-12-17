#/usr/local/bin/python3
from bkng.infra.db.dbconnectionmanager import DBConnectionManager
cm=DBConnectionManager()
# read only database connection 
android_ro=cm.get_connection('android','ro')

######################################################
# TODO
# check configuration files
# - FirebaseCrashH2/secrets/booking.com/db.json
# - FirebaseCrashH2/pool_roster/androiddb-dqs_set
######################################################

##################################################
# read only database connection 
#################################################
# database description
#a=android_ro.execute("DESC firebase_crashlytics_com_booking_ANDROID;")
# [Jia] DB access slow, excluding 'threads' speed up lots  
a=android_ro.execute("select issue_id,issue_title,issue_subtitle,exceptions,received_timestamp,application,\
	 from firebase_crashlytics_com_booking_ANDROID limit 5;")
# get crash log 2 days ago
oneold_item=android_ro.execute('select issue_id,received_timestamp,event_timestamp from firebase_crashlytics_com_booking_ANDROID where received_timestamp<DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 2 DAY);')

##################################################
# read/write database connection 
##################################################
android_rw=cm.get_connection('android','rw')

# database description
# [Jia] DB access slow, excluding 'threads' speed up lots  
a=android_rw.execute("select issue_id,issue_title,issue_subtitle,exceptions,received_timestamp,application,\
	 from firebase_crashlytics_com_booking_ANDROID limit 5;")
# get crash log 2 days ago
oneold_item=android_rw.execute('select issue_id,received_timestamp,event_timestamp from firebase_crashlytics_com_booking_ANDROID where received_timestamp<DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 2 DAY);')
