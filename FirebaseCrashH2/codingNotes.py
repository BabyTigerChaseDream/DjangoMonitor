
'''
[Requests on retrieve data]
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