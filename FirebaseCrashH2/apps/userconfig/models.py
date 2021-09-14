# Create your models here.
from django.db import models

from django.core.exceptions import ObjectDoesNotExist



class Config(models.Model):
	id = models.AutoField(primary_key=True)
	team = models.CharField(max_length=255)
	team_id = models.CharField(max_length=255)
	contacts = models.CharField(max_length=600, default=None)
	slack_channel = models.CharField(max_length=600, default=None)
	email_address = models.CharField(max_length=600, default=None)
	crash_count = models.IntegerField(default=0)
	total_users = models.IntegerField(default=0)
	# TODO: splitter
	files = models.CharField(max_length=2000, default=None)
	# TODO: splitter
	keywords = models.CharField(max_length=2000, default=None) 
	tags = models.CharField(max_length=600, default=None)

	'''
	CREATE TABLE if not exists `Config` (
	    `id` INT NOT NULL AUTO_INCREMENT,
	    `team` varchar(255) NOT NULL,
	    `team_id` varchar(255) DEFAULT '0',
	    `contacts` varchar(600) DEFAULT NULL,
	    `slack_channel` varchar(600) DEFAULT NULL,
	    `email_address` varchar(600) DEFAULT NULL,
	    `crash_count` int(10) unsigned NOT NULL DEFAULT '0',
	    `total_users` int(10) unsigned NOT NULL DEFAULT '0',
	    `files` varchar(2000) DEFAULT NULL,
	    `keywords` varchar(2000) DEFAULT NULL,
		`tags` varchar(600) DEFAULT NULL,
	     PRIMARY KEY (id)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;
	'''
	def __str__(self): 
		return '%s - %s ([%s]:[user]%s:[crashes]%s)' % \
			(self.issue_id, self.title, self.event_timestamp, self.total_users, self.crash_count)

	def create(self, **kwargs): 
	    team_id = kwargs['issue_id']
	    slack_channel = kwargs['slack_channel'] 
	    email_address = kwargs['email_address'] 

	    try:
	    	obj=self.objects.get(team_id=team_id, slack_channel=slack_channel, email_address=email_address)
	    except ObjectDoesNotExist:
		    obj=self.objects.create(**kwargs)
		    obj.save()
	    return obj

	def update(self, **kwargs): 
	    obj, created = self.objects.update_or_create(**kwargs)
	    if created:
		    obj.save()
	    return obj