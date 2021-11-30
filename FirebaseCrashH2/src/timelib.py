from datetime import datetime, timedelta
import common_config 
class timestamp:
	DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
	def __init__(self,date_format=DATE_FORMAT):
		self.date_format = date_format

	def timeslot(self, end_date=datetime.utcnow(), delta=common_config.delta_timeslot):
		date_format =  self.DATE_FORMAT 
		end_datetime = (datetime.utcnow() - timedelta(days=1))
		start_datetime = (datetime.utcnow() - timedelta(days=1+delta))
		self.start_timestamp_str = start_datetime.strftime(date_format)
		self.end_timestamp_str = end_datetime.strftime(date_format) 
		return self.start_timestamp_str,self.end_timestamp_str

	def timeslotbymin(self, end_date=datetime.utcnow(), delta=30):
		date_format =  self.DATE_FORMAT 
		end_datetime = (datetime.utcnow())
		start_datetime = (datetime.utcnow() - timedelta(minutes=delta))
		self.start_timestamp_str = start_datetime.strftime(date_format)
		self.end_timestamp_str = end_datetime.strftime(date_format) 
		return self.start_timestamp_str,self.end_timestamp_str

	def strp2date(self,timestr:str,date_format=None)->datetime:
		''' string to datetime '''
		if not date_format:
			date_format = self.DATE_FORMAT
		return datetime.strptime(timestr,format)
	
	def strf2str(self,timedate:datetime,date_format=None)->str:
		''' datetime to string '''
		if not date_format:
			date_format = self.DATE_FORMAT
		return timedate.strftime(format)

	