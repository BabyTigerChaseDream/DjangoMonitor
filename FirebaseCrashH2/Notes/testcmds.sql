### select all issue related data from database table 
# [cmd-1] specific app version 
'''
additional_where_clause=f"and application.display_version = \"{app_version}\""

SELECT 
  q1.issue_id,
  q1.issue_title,
  q1.issue_subtitle,
  q1.ticket_id,
  q1.app_versions,
  q1.events,
  q1.users,
  q2.total_events,
  q2.total_users,
  q2.total_issues
FROM (
    SELECT
      issues.issue_id as issue_id,
      issues.issue_title as issue_title,
      issues.issue_subtitle as issue_subtitle,
      tickets.ticket_id as ticket_id,
      array_agg(DISTINCT issues.application.display_version) AS app_versions,
      COUNT(DISTINCT event_id) AS events,
      COUNT(DISTINCT installation_uuid) AS users
    FROM `{table}*` issues, UNNEST(custom_keys)
    LEFT JOIN
     `{table_metadata}` tickets ON tickets.issue_id = issues.issue_id
    WHERE
      is_fatal=@is_fatal and event_timestamp >= @event_timestamp_start and event_timestamp <= @event_timestamp_end {additional_where_clause}
    GROUP BY
      issue_id, issue_title, issue_subtitle, ticket_id 
    ORDER BY
      users DESC
    LIMIT @limit OFFSET @offset
    ) as q1,
    (
        SELECT
            COUNT(DISTINCT issue_id) AS total_issues,
            COUNT(DISTINCT event_id) AS total_events,
            COUNT(DISTINCT installation_uuid) AS total_users
        FROM `{table}*`
        WHERE
            is_fatal=@is_fatal and event_timestamp >= @event_timestamp_start and event_timestamp <= @event_timestamp_end {additional_where_clause}
    ) as q2
'''

# [cmd-2]  all app versions  
'''
SELECT 
  q1.issue_id,
  q1.issue_title,
  q1.issue_subtitle,
  q1.ticket_id,
  q1.app_versions,
  q1.events,
  q1.users,
  q2.total_events,
  q2.total_users,
  q2.total_issues
FROM (
    SELECT
      issues.issue_id as issue_id,
      issues.issue_title as issue_title,
      issues.issue_subtitle as issue_subtitle,
      tickets.ticket_id as ticket_id,
      array_agg(DISTINCT issues.application.display_version) AS app_versions,
      COUNT(DISTINCT event_id) AS events,
      COUNT(DISTINCT installation_uuid) AS users
    FROM `firebase_crashlytics_com_booking_ANDROID` issues, UNNEST(custom_keys)
    LEFT JOIN
     `firebase_crashlytics_jira_sync` tickets ON tickets.issue_id = issues.issue_id
    WHERE
      is_fatal=@is_fatal and event_timestamp >= @event_timestamp_start and event_timestamp <= @event_timestamp_end
    GROUP BY
      issue_id, issue_title, issue_subtitle, ticket_id 
    ORDER BY
      users DESC
    LIMIT @limit OFFSET @offset
    ) as q1,
    (
        SELECT
            COUNT(DISTINCT issue_id) AS total_issues,
            COUNT(DISTINCT event_id) AS total_events,
            COUNT(DISTINCT installation_uuid) AS total_users
        FROM `firebase_crashlytics_com_booking_ANDROID`
        WHERE
            is_fatal=@is_fatal and event_timestamp >= @event_timestamp_start and event_timestamp <= @event_timestamp_end
    ) as q2
'''

''' ======= liner cmd generate date ====== '''
from datetime import datetime, timedelta
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

start_datetime = (datetime.utcnow() - timedelta(days=1))
end_datetime = datetime.utcnow()

date_str = start_datetime.strftime(DATE_FORMAT)
date_end_str = end_datetime.strftime(DATE_FORMAT)

'''***** [table q1] ******'''
SELECT issues.issue_id as issue_id, issues.issue_title as issue_title, issues.issue_subtitle as issue_subtitle, tickets.ticket_id as ticket_id, 
	'array_agg(DISTINCT issues.application.display_version) AS app_versions, '
	COUNT(DISTINCT event_id) AS events, COUNT(DISTINCT installation_uuid) AS users
FROM `firebase_crashlytics_com_booking_ANDROID*` issues, UNNEST(custom_keys)
LEFT JOIN
`firebase_crashlytics_jira_sync` tickets ON tickets.issue_id = issues.issue_id
WHERE event_timestamp >= '2021-07-20 12:58:50' and event_timestamp <= '2021-17-20 19:58:50'
GROUP BY issue_id, issue_title, issue_subtitle, ticket_id 
ORDER BY users DESC LIMIT 10 
'LIMIT @limit OFFSET @offset'

'''***** [table q2] *****'''
SELECT COUNT(DISTINCT issue_id) AS total_issues, COUNT(DISTINCT event_id) AS total_events, COUNT(DISTINCT installation_uuid) AS total_users
FROM `firebase_crashlytics_com_booking_ANDROID`
WHERE event_timestamp >= '2021-07-20 09:58:50' and event_timestamp <= '2021-07-20 19:58:50'
'WHERE is_fatal=@is_fatal and event_timestamp >= '2021-07-20 09:58:50' and event_timestamp <= '2021-07-20 19:58:50'

##################################################################
    Where clause filter crashes - only for col (NOT for alias)
##################################################################

select issue_id, count(distinct event_id) as crash_count, count(distinct installation_uuid) as total_users from `firebase_crashlytics_com_booking_ANDROID` 
  where event_timestamp >= '2021-07-20 09:58:50' and event_timestamp <= '2021-07-20 19:58:50' group by issue_id order by total_users desc limit 10;
+----------------------------------+--------------+-------------+
| issue_id                         | total_events | total_users |
+----------------------------------+--------------+-------------+
| 5c06a163f8b88c296382cb87         | 97           | 97          |
| a90e5206fb185ba394bb890f4a0b74ba | 144          | 86          |
| 57d315f90aeb16625bf85353         | 79           | 79          |
| ae2c21e4871b7d28d8f50cd0f9a310cc | 92           | 34          |
| f60005b8140e060a4111d9ba53ac18bb | 29           | 26          |
| 8fbf9fa572753f95b47cc0796abf0a61 | 23           | 22          |
| 0194d93e80614b77dc6413f32e295f14 | 26           | 22          |
| 4bc0978871cc4e7e29ee6398b786869f | 22           | 22          |
| 81078954a279a362b6703a92309ba8a1 | 16           | 16          |
| 5c63e39ff8b88c2963a80ddd         | 21           | 14          |
+----------------------------------+--------------+-------------+
10 rows in set
Time: 0.259s

##################################################################
Having clause filter crashes: on alias must use having to filter 
##################################################################
##################################################################
		DECIMAL convert-a-string-to-a-float 
##################################################################
DECIMAL on the CAST() :
	DECIMAL[(M[,D])]
	Converts a value to DECIMAL data type. The optional arguments M and D specify the precision (M specifies the total number of digits) and the scale (D specifies the number of digits after the decimal point) of the decimal value. The default precision is two digits after the decimal point.

android(ro)> select issue_id, application->'$.display_version' as app_version,count(distinct event_id) as crash_count, count(distinct installation_uuid) as total_users
				from `firebase_crashlytics_com_booking_ANDROID`
				where event_timestamp >= '2021-07-26 00:00:00' and event_timestamp <= '2021-07-26 23:59:59'
				group by issue_id
				having crash_count>100 and total_users>50 and CAST(app_version AS DECIMAL(10,3))>26
				order by total_users desc limit 10;
	+----------------------------------+-------------+-------------+-------------+
	| issue_id                         | app_version | crash_count | total_users |
	+----------------------------------+-------------+-------------+-------------+
	| 5d2c6080e0c9ddb395fefb721174fdaf | "28.1"      | 1127        | 778         |
	| 07097b4a18819ee555ab639dfc558b8f | "28.1"      | 1036        | 329         |
	| 5c06a163f8b88c296382cb87         | "28.1"      | 194         | 193         |
	| a90e5206fb185ba394bb890f4a0b74ba | "28.1"      | 189         | 140         |
	| a161fb36de87471568fafc656965f7ba | "28.1"      | 418         | 65          |
	+----------------------------------+-------------+-------------+-------------+
	5 rows in set
Time: 0.786s

##################################################################
'''***** Get Crash app version array [table Q3] *****'''
##################################################################
# version contains repeated app versions
  select issue_id, JSON_ARRAYAGG(application->'$.display_version') as app_versions from `firebase_crashlytics_com_booking_ANDROID` where event_timestamp >= '2021-07-20 09:58:50' and event_timestamp <= '2021-07-20 19:58:50' limit 5;
# version contains only distinct app versions
  select issue_id, JSON_ARRAYAGG(application->'$.display_version') as app_versions from `firebase_crashlytics_com_booking_ANDROID` where event_timestamp >= '2021-07-20 09:58:50' and event_timestamp <= '2021-07-20 19:58:50' limit 5;

# after retrieve issue_id of top crashes and users 
# get crash/issue code level detail from request :
template : https://ota.booking.com/crashes/Android/stacktraces?issue_ids={issue_id}&cached=true&start_date=&end_date
# select frame 
# - 'symbol' session in each frames is source code 
# - 'owner' is "DEVELOPER" message will be displayed in black , 'SYSTEM' owner will be display in grey

[Example]
https://ota.booking.com/crashes/Android/stacktraces?issue_ids=5d2c6080e0c9ddb395fefb721174fdaf&cached=true&start_date=&end_date
  - returning data return in request above maps to 'firebase_crashlytics_com_booking_ANDROID' blame_frame 
  {
    address: null,
    blamed: true,
    code_owners: [ ],
    file: "BuiPaginationIndicator.java",
    gitlab_commit: { },
    gitlab_link: "",
    library: "com.booking",
    line: 290,
    offset: 290,
    owner: "DEVELOPER",
    symbol: "bui.android.component.pagination.indicator.BuiPaginationIndicator.setCurrentPosition"
  }


#################################
##### [TODO] find 'crashes' ##### 
#################################
Find versions information from :
/Users/jiaguo/workspace/release-page/app_operations/releaser/templates/crashes/issue_card.html
Code temp:

                <div class="col issue-header-element">
                    <p class="issue-header-element text-center" style="color:rgba(0,0,0,.54)">Versions</p>
                    {% if versions|length > 1 %}
                        <p class="issue-header-element text-center">{{ versions[0]}} .. {{ versions[-1]}}</p>
                    {% else %}
                        <p class="issue-header-element text-center">{{ versions[0] }}</p>
                    {% endif %}
                </div>

[SQL CMD to find all application.display_versions - all crash versions]
