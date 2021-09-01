###### start steps #######

>>> dblib.DBEngine.execute(raw_cmd)
<sqlalchemy.engine.cursor.LegacyCursorResult object at 0x7fc6f509da10>
>>> 
>>> cdata=dblib.DBEngine.execute(raw_cmd)

#######################################################
#Find all not null exceptions in all installation_ids
#######################################################
sql_cmd_issue_stackframe='''select issue_id,count(distinct event_id) as crash_count,count(distinct installation_uuid) as total_users from `firebase_crashlytics_com_booking_ANDROID` where event_timestamp >= '2021-08-20 03:45:21' and event_timestamp <= '2021-08-29 03:45:21'and issue_id='5c06a163f8b88c296382cb87';'''
cursor=dblib.DBEngine.execute(sql_cmd_issue_stackframe)

>>> cursor.fetchone()
('5c06a163f8b88c296382cb87', 5572, 5283, '[{"type": "java.lang.IllegalArgumentException", "title": "Fatal Exception: java.lang.IllegalArgumentException", "blamed": true, "frames": [{"file": " ... (2653 characters truncated) ... essage": "reportSizeConfigurations: ActivityRecord not found for: Token{a43e43e ActivityRecord{939cf9 u0 com.booking/.startup.HomeActivity t-1 f}}"}]', None)
>>> cursor=dblib.DBEngine.execute(sql_cmd_issue_stackframe)
>>> crash_content=cursor.fetchone()
>>> crash_content.items()
__main__:1: SADeprecationWarning: The LegacyRow.items() method is deprecated and will be removed in a future release.  Use the Row._mapping attribute, i.e., 'row._mapping.items()'. (deprecated since: 1.4)
[('issue_id', '5c06a163f8b88c296382cb87'), ('crash_count', 5572), ('total_users', 5283), ('exceptions', '[{"type": "java.lang.IllegalArgumentException", "title": "Fatal Exception: java.lang.IllegalArgumentException", "blamed": true, "frames": [{"file": "Parcel.java", "line": 1958, "owner": "SYSTEM", "blamed": false, "offset": 1958, "symbol": "android.os.Parcel.readException", "address": null, "library": "com.booking"}, {"file": "Parcel.java", "line": 1900, "owner": "SYSTEM", "blamed": false, "offset": 1900, "symbol": "android.os.Parcel.readException", "address": null, "library": "com.booking"}, {"file": "IActivityManager.java", "line": 9358, "owner": "SYSTEM", "blamed": false, "offset": 9358, "symbol": "android.app.IActivityManager$Stub$Proxy.reportSizeConfigurations", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 3478, "owner": "SYSTEM", "blamed": true, "offset": 3478, "symbol": "android.app.ActivityThread.reportSizeConfigurations", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 3421, "owner": "SYSTEM", "blamed": false, "offset": 3421, "symbol": "android.app.ActivityThread.handleLaunchActivity", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": null, "owner": "SYSTEM", "blamed": false, "offset": null, "symbol": "android.app.ActivityThread.-wrap12", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 1994, "owner": "SYSTEM", "blamed": false, "offset": 1994, "symbol": "android.app.ActivityThread$H.handleMessage", "address": null, "library": "com.booking"}, {"file": "Handler.java", "line": 108, "owner": "SYSTEM", "blamed": false, "offset": 108, "symbol": "android.os.Handler.dispatchMessage", "address": null, "library": "com.booking"}, {"file": "Looper.java", "line": 166, "owner": "SYSTEM", "blamed": false, "offset": 166, "symbol": "android.os.Looper.loop", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 7529, "owner": "SYSTEM", "blamed": false, "offset": 7529, "symbol": "android.app.ActivityThread.main", "address": null, "library": "com.booking"}, {"file": "Method.java", "line": null, "owner": "SYSTEM", "blamed": false, "offset": null, "symbol": "java.lang.reflect.Method.invoke", "address": null, "library": "com.booking"}, {"file": "Zygote.java", "line": 245, "owner": "SYSTEM", "blamed": false, "offset": 245, "symbol": "com.android.internal.os.Zygote$MethodAndArgsCaller.run", "address": null, "library": "com.booking"}, {"file": "ZygoteInit.java", "line": 921, "owner": "SYSTEM", "blamed": false, "offset": 921, "symbol": "com.android.internal.os.ZygoteInit.main", "address": null, "library": "com.booking"}], "nested": false, "subtitle": "reportSizeConfigurations: ActivityRecord not found for: Token{a43e43e ActivityRecord{939cf9 u0 com.booking/.startup.HomeActivity t-1 f}}", "exception_message": "reportSizeConfigurations: ActivityRecord not found for: Token{a43e43e ActivityRecord{939cf9 u0 com.booking/.startup.HomeActivity t-1 f}}"}]'), ('blame_frame', None)]
>>> issue_exceptions=crash_content['exceptions']
>>> issue_exceptions
'[{"type": "java.lang.IllegalArgumentException", "title": "Fatal Exception: java.lang.IllegalArgumentException", "blamed": true, "frames": [{"file": "Parcel.java", "line": 1958, "owner": "SYSTEM", "blamed": false, "offset": 1958, "symbol": "android.os.Parcel.readException", "address": null, "library": "com.booking"}, {"file": "Parcel.java", "line": 1900, "owner": "SYSTEM", "blamed": false, "offset": 1900, "symbol": "android.os.Parcel.readException", "address": null, "library": "com.booking"}, {"file": "IActivityManager.java", "line": 9358, "owner": "SYSTEM", "blamed": false, "offset": 9358, "symbol": "android.app.IActivityManager$Stub$Proxy.reportSizeConfigurations", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 3478, "owner": "SYSTEM", "blamed": true, "offset": 3478, "symbol": "android.app.ActivityThread.reportSizeConfigurations", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 3421, "owner": "SYSTEM", "blamed": false, "offset": 3421, "symbol": "android.app.ActivityThread.handleLaunchActivity", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": null, "owner": "SYSTEM", "blamed": false, "offset": null, "symbol": "android.app.ActivityThread.-wrap12", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 1994, "owner": "SYSTEM", "blamed": false, "offset": 1994, "symbol": "android.app.ActivityThread$H.handleMessage", "address": null, "library": "com.booking"}, {"file": "Handler.java", "line": 108, "owner": "SYSTEM", "blamed": false, "offset": 108, "symbol": "android.os.Handler.dispatchMessage", "address": null, "library": "com.booking"}, {"file": "Looper.java", "line": 166, "owner": "SYSTEM", "blamed": false, "offset": 166, "symbol": "android.os.Looper.loop", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 7529, "owner": "SYSTEM", "blamed": false, "offset": 7529, "symbol": "android.app.ActivityThread.main", "address": null, "library": "com.booking"}, {"file": "Method.java", "line": null, "owner": "SYSTEM", "blamed": false, "offset": null, "symbol": "java.lang.reflect.Method.invoke", "address": null, "library": "com.booking"}, {"file": "Zygote.java", "line": 245, "owner": "SYSTEM", "blamed": false, "offset": 245, "symbol": "com.android.internal.os.Zygote$MethodAndArgsCaller.run", "address": null, "library": "com.booking"}, {"file": "ZygoteInit.java", "line": 921, "owner": "SYSTEM", "blamed": false, "offset": 921, "symbol": "com.android.internal.os.ZygoteInit.main", "address": null, "library": "com.booking"}], "nested": false, "subtitle": "reportSizeConfigurations: ActivityRecord not found for: Token{a43e43e ActivityRecord{939cf9 u0 com.booking/.startup.HomeActivity t-1 f}}", "exception_message": "reportSizeConfigurations: ActivityRecord not found for: Token{a43e43e ActivityRecord{939cf9 u0 com.booking/.startup.HomeActivity t-1 f}}"}]'
>>> import json
>>> json.loads(issue_exceptions)
[{'type': 'java.lang.IllegalArgumentException', 'title': 'Fatal Exception: java.lang.IllegalArgumentException', 'blamed': True, 'frames': [{'file': 'Parcel.java', 'line': 1958, 'owner': 'SYSTEM', 'blamed': False, 'offset': 1958, 'symbol': 'android.os.Parcel.readException', 'address': None, 'library': 'com.booking'}, {'file': 'Parcel.java', 'line': 1900, 'owner': 'SYSTEM', 'blamed': False, 'offset': 1900, 'symbol': 'android.os.Parcel.readException', 'address': None, 'library': 'com.booking'}, {'file': 'IActivityManager.java', 'line': 9358, 'owner': 'SYSTEM', 'blamed': False, 'offset': 9358, 'symbol': 'android.app.IActivityManager$Stub$Proxy.reportSizeConfigurations', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 3478, 'owner': 'SYSTEM', 'blamed': True, 'offset': 3478, 'symbol': 'android.app.ActivityThread.reportSizeConfigurations', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 3421, 'owner': 'SYSTEM', 'blamed': False, 'offset': 3421, 'symbol': 'android.app.ActivityThread.handleLaunchActivity', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': None, 'owner': 'SYSTEM', 'blamed': False, 'offset': None, 'symbol': 'android.app.ActivityThread.-wrap12', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 1994, 'owner': 'SYSTEM', 'blamed': False, 'offset': 1994, 'symbol': 'android.app.ActivityThread$H.handleMessage', 'address': None, 'library': 'com.booking'}, {'file': 'Handler.java', 'line': 108, 'owner': 'SYSTEM', 'blamed': False, 'offset': 108, 'symbol': 'android.os.Handler.dispatchMessage', 'address': None, 'library': 'com.booking'}, {'file': 'Looper.java', 'line': 166, 'owner': 'SYSTEM', 'blamed': False, 'offset': 166, 'symbol': 'android.os.Looper.loop', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 7529, 'owner': 'SYSTEM', 'blamed': False, 'offset': 7529, 'symbol': 'android.app.ActivityThread.main', 'address': None, 'library': 'com.booking'}, {'file': 'Method.java', 'line': None, 'owner': 'SYSTEM', 'blamed': False, 'offset': None, 'symbol': 'java.lang.reflect.Method.invoke', 'address': None, 'library': 'com.booking'}, {'file': 'Zygote.java', 'line': 245, 'owner': 'SYSTEM', 'blamed': False, 'offset': 245, 'symbol': 'com.android.internal.os.Zygote$MethodAndArgsCaller.run', 'address': None, 'library': 'com.booking'}, {'file': 'ZygoteInit.java', 'line': 921, 'owner': 'SYSTEM', 'blamed': False, 'offset': 921, 'symbol': 'com.android.internal.os.ZygoteInit.main', 'address': None, 'library': 'com.booking'}], 'nested': False, 'subtitle': 'reportSizeConfigurations: ActivityRecord not found for: Token{a43e43e ActivityRecord{939cf9 u0 com.booking/.startup.HomeActivity t-1 f}}', 'exception_message': 'reportSizeConfigurations: ActivityRecord not found for: Token{a43e43e ActivityRecord{939cf9 u0 com.booking/.startup.HomeActivity t-1 f}}'}]

'''
#########################################
######  [Requests retrieve data]   ######
#########################################

- default crash data : https://ota.booking.com/crashes/
- customized data: https://ota.booking.com/crashes/?project_name=Android&interval=1h&page_no=0&app_version=v27.9&issue_type=Crash
- retrieve jira ID - from source page: 
  in page source : view-source:https://ota.booking.com/crashes/
  ---
    search for data-issue_id="fa49a3e8e23c3c431b0b59e5b0d5d9e9" 
  ---
    <a class="col stack-trace-title external" target="_blank"
    	href="https://console.firebase.google.com/project/booking-oauth/crashlytics/app/android:com.booking/issues/fa49a3e8e23c3c431b0b59e5b0d5d9e9 ">Presenter.java line 799</a>
    <p class="col stack-trace-subtitle text-break">com.booking.postbooking.modifybooking.Presenter.contactProperty</p>

- retrieve single crash detail data:
  #https://ota.booking.com/crashes/Android/stacktraces?issue_ids=57d315f90aeb16625bf85353&cached=true&start_date=&end_date
  https://ota.booking.com/crashes/Android/{issue_id}

#####################################################
#### [retrieve stacktrace: db COL => exceptions ] ####
#####################################################
**************

[KEY]: application
 [V]: {"build_version": "14733", "display_version": "27.9"}
**********

[KEY]: exceptions
 [V]: [{"type": "java.lang.ClassCastException", "title": "Fatal Exception: java.lang.ClassCastException", "blamed": true, "frames": [{"file": "SimpleArrayMap.java", "line": 184, "owner": "SYSTEM", "blamed": false, "offset": 18
4, "symbol": "androidx.collection.SimpleArrayMap.allocArrays", "address": null, "library": "com.booking"}, {"file": "SimpleArrayMap.java", "line": 458, "owner": "SYSTEM", "blamed": false, "offset": 458, "symbol": "androidx.col
lection.SimpleArrayMap.put", "address": null, "library": "com.booking"}, {"file": "TTracer.java", "line": 147, "owner": "DEVELOPER", "blamed": true, "offset": 147, "symbol": "com.booking.transmon.tti.TTracer.innerTrace", "addr
ess": null, "library": "com.booking"}, {"file": "TTracer.java", "line": 81, "owner": "DEVELOPER", "blamed": false, "offset": 81, "symbol": "com.booking.transmon.tti.TTracer.trace", "address": null, "library": "com.booking"}, {
"file": "HotelActivity.java", "line": 1388, "owner": "DEVELOPER", "blamed": false, "offset": 1388, "symbol": "com.booking.property.detail.HotelActivity.trackBackToSearchResults", "address": null, "library": "com.booking"}, {"f
ile": "HotelActivity.java", "line": 1126, "owner": "DEVELOPER", "blamed": false, "offset": 1126, "symbol": "com.booking.property.detail.HotelActivity.goUp", "address": null, "library": "com.booking"}, {"file": "BaseActivity.ja
va", "line": 219, "owner": "DEVELOPER", "blamed": false, "offset": 219, "symbol": "com.booking.commonui.activity.BaseActivity.onOptionsItemSelected", "address": null, "library": "com.booking"}, {"file": "HotelActivity.java", "
line": 1119, "owner": "DEVELOPER", "blamed": false, "offset": 1119, "symbol": "com.booking.property.detail.HotelActivity.onOptionsItemSelected", "address": null, "library": "com.booking"}, {"file": "Activity.java", "line": 363
0, "owner": "SYSTEM", "blamed": false, "offset": 3630, "symbol": "android.app.Activity.onMenuItemSelected", "address": null, "library": "com.booking"}, {"file": "FragmentActivity.java", "line": 383, "owner": "SYSTEM", "blamed"
: false, "offset": 383, "symbol": "androidx.fragment.app.FragmentActivity.onMenuItemSelected", "address": null, "library": "com.booking"}, {"file": "AppCompatActivity.java", "line": 228, "owner": "SYSTEM", "blamed": false, "of
fset": 228, "symbol": "androidx.appcompat.app.AppCompatActivity.onMenuItemSelected", "address": null, "library": "com.booking"}, {"file": "WindowCallbackWrapper.java", "line": 109, "owner": "SYSTEM", "blamed": false, "offset":
 109, "symbol": "androidx.appcompat.view.WindowCallbackWrapper.onMenuItemSelected", "address": null, "library": "com.booking"}, {"file": "ToolbarWidgetWrapper.java", "line": 188, "owner": "SYSTEM", "blamed": false, "offset": 1
88, "symbol": "androidx.appcompat.widget.ToolbarWidgetWrapper$1.onClick", "address": null, "library": "com.booking"}, {"file": "View.java", "line": 7339, "owner": "SYSTEM", "blamed": false, "offset": 7339, "symbol": "android.v
iew.View.performClick", "address": null, "library": "com.booking"}, {"file": "View.java", "line": 7305, "owner": "SYSTEM", "blamed": false, "offset": 7305, "symbol": "android.view.View.performClickInternal", "address": null, "
library": "com.booking"}, {"file": "View.java", "line": 846, "owner": "SYSTEM", "blamed": false, "offset": 846, "symbol": "android.view.View.access$3200", "address": null, "library": "com.booking"}, {"file": "View.java", "line
": 27787, "owner": "SYSTEM", "blamed": false, "offset": 27787, "symbol": "android.view.View$PerformClick.run", "address": null, "library": "com.booking"}, {"file": "Handler.java", "line": 873, "owner": "SYSTEM", "blamed": fals
e, "offset": 873, "symbol": "android.os.Handler.handleCallback", "address": null, "library": "com.booking"}, {"file": "Handler.java", "line": 99, "owner": "SYSTEM", "blamed": false, "offset": 99, "symbol": "android.os.Handler.
dispatchMessage", "address": null, "library": "com.booking"}, {"file": "Looper.java", "line": 214, "owner": "SYSTEM", "blamed": false, "offset": 214, "symbol": "android.os.Looper.loop", "address": null, "library": "com.booking
"}, {"file": "ActivityThread.java", "line": 7077, "owner": "SYSTEM", "blamed": false, "offset": 7077, "symbol": "android.app.ActivityThread.main", "address": null, "library": "com.booking"}, {"file": "Method.java", "line": nul
l, "owner": "SYSTEM", "blamed": false, "offset": null, "symbol": "java.lang.reflect.Method.invoke", "address": null, "library": "com.booking"}, {"file": "RuntimeInit.java", "line": 494, "owner": "SYSTEM", "blamed": false, "off
set": 494, "symbol": "com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run", "address": null, "library": "com.booking"}, {"file": "ZygoteInit.java", "line": 964, "owner": "SYSTEM", "blamed": false, "offset": 964, "symbo
l": "com.android.internal.os.ZygoteInit.main", "address": null, "library": "com.booking"}], "nested": false, "subtitle": "com.booking.pob.data.PobParams cannot be cast to java.lang.Object[]", "exception_message": "com.booking.
pob.data.PobParams cannot be cast to java.lang.Object[]"}]
**********

[KEY]: blame_frame
 [V]: {"file": "TTracer.java", "line": 147, "owner": "DEVELOPER", "blamed": true, "offset": 147, "symbol": "com.booking.transmon.tti.TTracer.innerTrace", "address": null, "library": "com.booking"}

>>>

#########################################
######    [BS4 retrieve data]      ######
#########################################
- retrieve User being affected
1) BeautifulSoup find silbling div 
soup.find('div', text='Employee Count').find_next_sibling().text
[eg]
>>> from bs4 import BeautifulSoup
>>> data = """
... <body>
... <div class="label">Employee Count</div>
... <div class="field">331,000</div>
... </body>
... """
>>> 
>>> soup = BeautifulSoup(data)
>>> soup.find('div', text='Employee Count').find_next_sibling().text
331,000

2) source code 
app_operations/releaser/templates/crashes/issue_card_list.html
<code>
#crash_count=issue.events,
#user_count=issue.users,

/Users/jiaguo/workspace/release-page/app_operations/releaser/templates/crashes/issue_card.html
 <code>
 #<!-- user count -->
 # <div class="col issue-header-element">
 #     <p class="issue-header-element text-center" style="color:rgba(0,0,0,.54)">Users</p>
 #     <p class="issue-header-element text-center">{{ user_count }}</p>
 # </div>

'''
############################################################################
# Booking Python lib: bkng_infra_db
# LINK : 
# https://gitlab.booking.com/python/bkng/-/blob/master/infra/db/README.md
############################################################################

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


####################################################
# ORM guide on database table manupulation
####################################################

# Get existing database Table class in Engine 


#### string / json to dict 
>>> issue_content['exceptions']
'[{"type": "java.lang.RuntimeException", "title": "Fatal Exception: java.lang.RuntimeException", "blamed": false, "frames": [{"file": "ActivityThread.java", "line": 4910, "owner": "SYSTEM", "blamed": false, "offset": 4910, "symbol": "android.app.ActivityThread.performResumeActivity", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 4953, "owner": "SYSTEM", "blamed": false, "offset": 4953, "symbol": "android.app.ActivityThread.handleResumeActivity", "address": null, "library": "com.booking"}, {"file": "ResumeActivityItem.java", "line": 52, "owner": "SYSTEM", "blamed": false, "offset": 52, "symbol": "android.app.servertransaction.ResumeActivityItem.execute", "address": null, "library": "com.booking"}, {"file": "TransactionExecutor.java", "line": 190, "owner": "SYSTEM", "blamed": false, "offset": 190, "symbol": "android.app.servertransaction.TransactionExecutor.executeLifecycleState", "address": null, "library": "com.booking"}, {"file": "TransactionExecutor.java", "line": 105, "owner": "SYSTEM", "blamed": false, "offset": 105, "symbol": "android.app.servertransaction.TransactionExecutor.execute", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 2462, "owner": "SYSTEM", "blamed": false, "offset": 2462, "symbol": "android.app.ActivityThread$H.handleMessage", "address": null, "library": "com.booking"}, {"file": "Handler.java", "line": 110, "owner": "SYSTEM", "blamed": false, "offset": 110, "symbol": "android.os.Handler.dispatchMessage", "address": null, "library": "com.booking"}, {"file": "Looper.java", "line": 219, "owner": "SYSTEM", "blamed": false, "offset": 219, "symbol": "android.os.Looper.loop", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 8393, "owner": "SYSTEM", "blamed": false, "offset": 8393, "symbol": "android.app.ActivityThread.main", "address": null, "library": "com.booking"}, {"file": "Method.java", "line": null, "owner": "SYSTEM", "blamed": false, "offset": null, "symbol": "java.lang.reflect.Method.invoke", "address": null, "library": "com.booking"}, {"file": "RuntimeInit.java", "line": 513, "owner": "SYSTEM", "blamed": false, "offset": 513, "symbol": "com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run", "address": null, "library": "com.booking"}, {"file": "ZygoteInit.java", "line": 1055, "owner": "SYSTEM", "blamed": false, "offset": 1055, "symbol": "com.android.internal.os.ZygoteInit.main", "address": null, "library": "com.booking"}], "nested": false, "subtitle": "Unable to resume activity {com.booking/com.booking.appindex.presentation.activity.SearchActivity}: kotlin.UninitializedPropertyAccessException: lateinit property reviewsAttentionHandler has not been initialized", "exception_message": "Unable to resume activity {com.booking/com.booking.appindex.presentation.activity.SearchActivity}: kotlin.UninitializedPropertyAccessException: lateinit property reviewsAttentionHandler has not been initialized"}, {"type": "kotlin.UninitializedPropertyAccessException", "title": "Caused by kotlin.UninitializedPropertyAccessException", "blamed": true, "frames": [{"file": "SearchActivity.java", "line": 466, "owner": "DEVELOPER", "blamed": true, "offset": 466, "symbol": "com.booking.appindex.presentation.activity.SearchActivity.onResume", "address": null, "library": "com.booking"}, {"file": "Instrumentation.java", "line": 1472, "owner": "SYSTEM", "blamed": false, "offset": 1472, "symbol": "android.app.Instrumentation.callActivityOnResume", "address": null, "library": "com.booking"}, {"file": "Activity.java", "line": 8258, "owner": "SYSTEM", "blamed": false, "offset": 8258, "symbol": "android.app.Activity.performResume", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 4900, "owner": "SYSTEM", "blamed": false, "offset": 4900, "symbol": "android.app.ActivityThread.performResumeActivity", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 4953, "owner": "SYSTEM", "blamed": false, "offset": 4953, "symbol": "android.app.ActivityThread.handleResumeActivity", "address": null, "library": "com.booking"}, {"file": "ResumeActivityItem.java", "line": 52, "owner": "SYSTEM", "blamed": false, "offset": 52, "symbol": "android.app.servertransaction.ResumeActivityItem.execute", "address": null, "library": "com.booking"}, {"file": "TransactionExecutor.java", "line": 190, "owner": "SYSTEM", "blamed": false, "offset": 190, "symbol": "android.app.servertransaction.TransactionExecutor.executeLifecycleState", "address": null, "library": "com.booking"}, {"file": "TransactionExecutor.java", "line": 105, "owner": "SYSTEM", "blamed": false, "offset": 105, "symbol": "android.app.servertransaction.TransactionExecutor.execute", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 2462, "owner": "SYSTEM", "blamed": false, "offset": 2462, "symbol": "android.app.ActivityThread$H.handleMessage", "address": null, "library": "com.booking"}, {"file": "Handler.java", "line": 110, "owner": "SYSTEM", "blamed": false, "offset": 110, "symbol": "android.os.Handler.dispatchMessage", "address": null, "library": "com.booking"}, {"file": "Looper.java", "line": 219, "owner": "SYSTEM", "blamed": false, "offset": 219, "symbol": "android.os.Looper.loop", "address": null, "library": "com.booking"}, {"file": "ActivityThread.java", "line": 8393, "owner": "SYSTEM", "blamed": false, "offset": 8393, "symbol": "android.app.ActivityThread.main", "address": null, "library": "com.booking"}, {"file": "Method.java", "line": null, "owner": "SYSTEM", "blamed": false, "offset": null, "symbol": "java.lang.reflect.Method.invoke", "address": null, "library": "com.booking"}, {"file": "RuntimeInit.java", "line": 513, "owner": "SYSTEM", "blamed": false, "offset": 513, "symbol": "com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run", "address": null, "library": "com.booking"}, {"file": "ZygoteInit.java", "line": 1055, "owner": "SYSTEM", "blamed": false, "offset": 1055, "symbol": "com.android.internal.os.ZygoteInit.main", "address": null, "library": "com.booking"}], "nested": true, "subtitle": "lateinit property reviewsAttentionHandler has not been initialized", "exception_message": "lateinit property reviewsAttentionHandler has not been initialized"}]'
>>> len(issue_content['exceptions'])
6312
>>> type(issue_content['exceptions'])
<class 'str'>
>>> import json
>>> except_dict=json.loads(issue_content['exceptions'])
>>> except_dict
[{'type': 'java.lang.RuntimeException', 'title': 'Fatal Exception: java.lang.RuntimeException', 'blamed': False, 'frames': [{'file': 'ActivityThread.java', 'line': 4910, 'owner': 'SYSTEM', 'blamed': False, 'offset': 4910, 'symbol': 'android.app.ActivityThread.performResumeActivity', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 4953, 'owner': 'SYSTEM', 'blamed': False, 'offset': 4953, 'symbol': 'android.app.ActivityThread.handleResumeActivity', 'address': None, 'library': 'com.booking'}, {'file': 'ResumeActivityItem.java', 'line': 52, 'owner': 'SYSTEM', 'blamed': False, 'offset': 52, 'symbol': 'android.app.servertransaction.ResumeActivityItem.execute', 'address': None, 'library': 'com.booking'}, {'file': 'TransactionExecutor.java', 'line': 190, 'owner': 'SYSTEM', 'blamed': False, 'offset': 190, 'symbol': 'android.app.servertransaction.TransactionExecutor.executeLifecycleState', 'address': None, 'library': 'com.booking'}, {'file': 'TransactionExecutor.java', 'line': 105, 'owner': 'SYSTEM', 'blamed': False, 'offset': 105, 'symbol': 'android.app.servertransaction.TransactionExecutor.execute', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 2462, 'owner': 'SYSTEM', 'blamed': False, 'offset': 2462, 'symbol': 'android.app.ActivityThread$H.handleMessage', 'address': None, 'library': 'com.booking'}, {'file': 'Handler.java', 'line': 110, 'owner': 'SYSTEM', 'blamed': False, 'offset': 110, 'symbol': 'android.os.Handler.dispatchMessage', 'address': None, 'library': 'com.booking'}, {'file': 'Looper.java', 'line': 219, 'owner': 'SYSTEM', 'blamed': False, 'offset': 219, 'symbol': 'android.os.Looper.loop', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 8393, 'owner': 'SYSTEM', 'blamed': False, 'offset': 8393, 'symbol': 'android.app.ActivityThread.main', 'address': None, 'library': 'com.booking'}, {'file': 'Method.java', 'line': None, 'owner': 'SYSTEM', 'blamed': False, 'offset': None, 'symbol': 'java.lang.reflect.Method.invoke', 'address': None, 'library': 'com.booking'}, {'file': 'RuntimeInit.java', 'line': 513, 'owner': 'SYSTEM', 'blamed': False, 'offset': 513, 'symbol': 'com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run', 'address': None, 'library': 'com.booking'}, {'file': 'ZygoteInit.java', 'line': 1055, 'owner': 'SYSTEM', 'blamed': False, 'offset': 1055, 'symbol': 'com.android.internal.os.ZygoteInit.main', 'address': None, 'library': 'com.booking'}], 'nested': False, 'subtitle': 'Unable to resume activity {com.booking/com.booking.appindex.presentation.activity.SearchActivity}: kotlin.UninitializedPropertyAccessException: lateinit property reviewsAttentionHandler has not been initialized', 'exception_message': 'Unable to resume activity {com.booking/com.booking.appindex.presentation.activity.SearchActivity}: kotlin.UninitializedPropertyAccessException: lateinit property reviewsAttentionHandler has not been initialized'}, {'type': 'kotlin.UninitializedPropertyAccessException', 'title': 'Caused by kotlin.UninitializedPropertyAccessException', 'blamed': True, 'frames': [{'file': 'SearchActivity.java', 'line': 466, 'owner': 'DEVELOPER', 'blamed': True, 'offset': 466, 'symbol': 'com.booking.appindex.presentation.activity.SearchActivity.onResume', 'address': None, 'library': 'com.booking'}, {'file': 'Instrumentation.java', 'line': 1472, 'owner': 'SYSTEM', 'blamed': False, 'offset': 1472, 'symbol': 'android.app.Instrumentation.callActivityOnResume', 'address': None, 'library': 'com.booking'}, {'file': 'Activity.java', 'line': 8258, 'owner': 'SYSTEM', 'blamed': False, 'offset': 8258, 'symbol': 'android.app.Activity.performResume', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 4900, 'owner': 'SYSTEM', 'blamed': False, 'offset': 4900, 'symbol': 'android.app.ActivityThread.performResumeActivity', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 4953, 'owner': 'SYSTEM', 'blamed': False, 'offset': 4953, 'symbol': 'android.app.ActivityThread.handleResumeActivity', 'address': None, 'library': 'com.booking'}, {'file': 'ResumeActivityItem.java', 'line': 52, 'owner': 'SYSTEM', 'blamed': False, 'offset': 52, 'symbol': 'android.app.servertransaction.ResumeActivityItem.execute', 'address': None, 'library': 'com.booking'}, {'file': 'TransactionExecutor.java', 'line': 190, 'owner': 'SYSTEM', 'blamed': False, 'offset': 190, 'symbol': 'android.app.servertransaction.TransactionExecutor.executeLifecycleState', 'address': None, 'library': 'com.booking'}, {'file': 'TransactionExecutor.java', 'line': 105, 'owner': 'SYSTEM', 'blamed': False, 'offset': 105, 'symbol': 'android.app.servertransaction.TransactionExecutor.execute', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 2462, 'owner': 'SYSTEM', 'blamed': False, 'offset': 2462, 'symbol': 'android.app.ActivityThread$H.handleMessage', 'address': None, 'library': 'com.booking'}, {'file': 'Handler.java', 'line': 110, 'owner': 'SYSTEM', 'blamed': False, 'offset': 110, 'symbol': 'android.os.Handler.dispatchMessage', 'address': None, 'library': 'com.booking'}, {'file': 'Looper.java', 'line': 219, 'owner': 'SYSTEM', 'blamed': False, 'offset': 219, 'symbol': 'android.os.Looper.loop', 'address': None, 'library': 'com.booking'}, {'file': 'ActivityThread.java', 'line': 8393, 'owner': 'SYSTEM', 'blamed': False, 'offset': 8393, 'symbol': 'android.app.ActivityThread.main', 'address': None, 'library': 'com.booking'}, {'file': 'Method.java', 'line': None, 'owner': 'SYSTEM', 'blamed': False, 'offset': None, 'symbol': 'java.lang.reflect.Method.invoke', 'address': None, 'library': 'com.booking'}, {'file': 'RuntimeInit.java', 'line': 513, 'owner': 'SYSTEM', 'blamed': False, 'offset': 513, 'symbol': 'com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run', 'address': None, 'library': 'com.booking'}, {'file': 'ZygoteInit.java', 'line': 1055, 'owner': 'SYSTEM', 'blamed': False, 'offset': 1055, 'symbol': 'com.android.internal.os.ZygoteInit.main', 'address': None, 'library': 'com.booking'}], 'nested': True, 'subtitle': 'lateinit property reviewsAttentionHandler has not been initialized', 'exception_message': 'lateinit property reviewsAttentionHandler has not been initialized'}]
>>> type(except_dict)
<class 'list'>

