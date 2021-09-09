from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Issue(models.Model):
    #issue_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.CharField(max_length=255)
    issue_title = models.CharField(max_length=255)
    issue_subtitle = models.CharField(max_length=255)
	# latest crash app version 
    app_version = models.CharField(max_length=255)
    crash_count = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
	# when this event happened 
    event_timestamp = models.TimeField()
    #retrieved_timestamp = models.TimeField() 
    logs = models.TextField()
    
    def __str__(self):
        return '%s - %s (%s:[user]%s:[crashes]%s)' % \
			(self.issue_id, self.title, self.event_timestamp, self.total_users, self.crash_count)