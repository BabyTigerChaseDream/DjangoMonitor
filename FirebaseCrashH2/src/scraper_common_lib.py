#import schedule 

#################################################################
# Cronjob: 
#################################################################

# TODO :
def job():
    # placeholder for jobs to retrieve android crash from kvm db
    pass 

schedule.every().day.at("06:30").do(job)

def https_get_stacktrace_frames_in_json(issue_id):
	crash_url = 'https://ota.booking.com/crashes/Android/stacktraces?issue_ids={issue_id}}&cached=true&start_date=&end_date'
	r= requests.get(crash_url)

	if r.status_code != 200:
		raise ValueError("HTTP request failed with errorcode: ", r.status_code)

	# get stacktrace->frames in response
	response = r.json()
	
	# frames(dict)
	response_frames = response['issues'][issue_id]['stacktrace']['frames']

	# frames(json)
	frames_in_json = json.dumps(response_frames)

	return frames_in_json

	# TODO: interace to store each item in local DB 

# [Jia] row["issue_id"] =>issues/{}
ISSUE_LINK = "https://console.firebase.google.com/project/booking-oauth/crashlytics/app/{}/issues/{} "