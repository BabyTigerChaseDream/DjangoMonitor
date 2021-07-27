
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
  https://ota.booking.com/crashes/Android/stacktraces?issue_ids=57d315f90aeb16625bf85353&cached=true&start_date=&end_date

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
