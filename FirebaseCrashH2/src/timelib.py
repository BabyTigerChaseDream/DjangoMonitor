from datetime import datetime, timedelta

class timestamp:
	DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
	def __init__(self,date_format=DATE_FORMAT):
		self.date_format = date_format

	def timeslot(self, end_date=datetime.utcnow(), delta=10):
		date_format =  self.DATE_FORMAT 
		end_datetime = (datetime.utcnow() - timedelta(days=10))
		start_datetime = (datetime.utcnow() - timedelta(days=12))
		#self.start_timestamp = start_datetime.strftime(date_format)
		#self.end_timestamp = end_datetime.strftime(date_format) 
		start_timestamp = start_datetime.strftime(date_format)
		end_timestamp = end_datetime.strftime(date_format) 
		return start_timestamp,end_timestamp
