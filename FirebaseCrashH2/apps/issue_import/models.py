from django.db import models

# Create your models here.
#from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist


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
    event_timestamp = models.CharField(max_length=255)
    #retrieved_timestamp = models.TimeField() 
    issue_logs = models.TextField(),
    app_version_list = models.TextField(),
    last_update_timestamp = models.CharField(max_length=255)	
    
	'''
	CREATE TABLE `Issue` (
		`issue_id` varchar(255) NOT NULL,
		`issue_title` varchar(500) DEFAULT NULL,
		`issue_subtitle` varchar(500) DEFAULT NULL,
		`app_version` varchar(255) DEFAULT NULL,
		`crash_count` int(10) unsigned NOT NULL DEFAULT '0',
		`total_user` int(10) unsigned NOT NULL DEFAULT '0',
		`event_timestamp` varchar(255) DEFAULT NULL,
		`issue_logs` text,
		`app_version_list` text,
		`last_update_timestamp` varchar(255) DEFAULT NULL,
		PRIMARY KEY (`issue_id`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC
	'''
    def __str__(self):
        return '%s - %s ([%s]:[user]%s:[crashes]%s)' % \
			(self.issue_id, self.title, self.event_timestamp, self.total_users, self.crash_count)

    def create(self, **kwargs): 
	    current_issue_id = kwargs['issue_id']
	    try:
	    	obj=self.objects.get(issue_id=current_issue_id)
			# new issue
			# new_issue_list.append(current_issue_id)
	    except ObjectDoesNotExist:
		    obj=self.objects.create(**kwargs)
		    obj.save()
	    return obj

    def update(self, **kwargs): 
	    #obj = None
	    obj, created = self.objects.update_or_create(**kwargs)
	    if created:
		    obj.save()
		# updated items is items consistently occur

	    return obj