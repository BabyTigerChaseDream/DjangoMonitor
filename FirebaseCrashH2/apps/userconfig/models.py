# Create your models here.
from django.db import models
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

PLATFORM_CHOICES = (
    ('android', 'android'),
    ('ios', 'ios')
)

class Config(models.Model):
	id = models.AutoField(primary_key=True)
	# help_text='your-lovely-teamname'
	team = models.CharField(max_length=255)
	
	#team_id = models.CharField(max_length=255, default='000000')
	
	#contacts = models.CharField(max_length=600, default='Jia Guo')
	#TODO
	platform = models.CharField(max_length=60, choices=PLATFORM_CHOICES, default='android') 
	#platform = models.CharField(max_length=60, default='android') 
	# help_text='slack-channel-to-receive-notification'
	slack_channel = models.CharField(max_length=600, default=None)

	email_address = models.CharField(max_length=600, default=None)
	crash_count = models.IntegerField(default=100)
	total_user = models.IntegerField(default=50)
	# TODO: splitter
	#files = models.CharField(max_length=2000, default=None, help_text='file names you wanna monitor ')
	files = models.CharField(max_length=2000, default=None)
	# TODO: splitter
	keywords = models.CharField(max_length=2000, default=None) 
	tags = models.CharField(max_length=600, default="Notes on this configuration")
	#start_date = models.DateTimeField(default=timezone.now()-timezone.timedelta(days=15) )
	timeslot = models.IntegerField(default=7)	
	end_date = models.DateTimeField(default=timezone.now) 
	# add one more fields: add all issue id list to corresponding userconfig  
	issue_id_list = models.CharField(max_length=2000, default='0000-0000-0000-0000') 
	issue_id_blacklist = models.CharField(max_length=500, default='0000-0000-0000-0000') 

	def __str__(self): 
		return '%s - %s (%s)' % \
			(self.id, self.team, self.issue_id_list)

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
'''

	CREATE TABLE if not exists `Config` (
	    `id` INT NOT NULL AUTO_INCREMENT,
	    `team` varchar(255) NOT NULL,
	    `team_id` varchar(255) DEFAULT '0',
	    `contacts` varchar(600) DEFAULT NULL,
	    `slack_channel` varchar(600) DEFAULT NULL,
	    `email_address` varchar(600) DEFAULT NULL,
	    `crash_count` int(10) unsigned NOT NULL DEFAULT '0',
	    `total_user` int(10) unsigned NOT NULL DEFAULT '0',
	    `files` varchar(2000) DEFAULT NULL,
	    `keywords` varchar(2000) DEFAULT NULL,
		`tags` varchar(600) DEFAULT NULL,
	     PRIMARY KEY (id)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

class UserCrash(models.Model):
    #issue_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.CharField(max_length=255)
    issue_title = models.CharField(max_length=255)
    issue_subtitle = models.CharField(max_length=255)
	# latest crash app version 
    app_version = models.CharField(max_length=255)
    crash_count = models.IntegerField(default=0)
    total_user = models.IntegerField(default=0)
	# when this event happened
    event_timestamp = models.CharField(max_length=255)
    #retrieved_timestamp = models.TimeField() 
    issue_logs = models.TextField(),
    app_version_list = models.TextField(),
    last_update_timestamp = models.CharField(max_length=255)

'''

class Crashissues(models.Model):
    issue_id = models.CharField(primary_key=True, max_length=255)
    issue_title = models.CharField(max_length=200, blank=True, null=True)
    issue_subtitle = models.CharField(max_length=200, blank=True, null=True)
    app_version = models.CharField(max_length=300, blank=True, null=True)
    platform=models.CharField(max_length=60, choices=PLATFORM_CHOICES, default='android')
    crash_count = models.PositiveIntegerField()
    total_user = models.PositiveIntegerField()
    event_timestamp = models.CharField(max_length=255, blank=True, null=True)
    issue_logs = models.TextField(blank=True, null=True)
    app_version_list = models.TextField(blank=True, null=True)
    last_update_timestamp = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CrashIssues'