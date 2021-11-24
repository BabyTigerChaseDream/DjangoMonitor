#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

setup_cron_job_completion = False 

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if not setup_cron_job_completion:
        print(">>>> Start Cron Job\n")
    	CronCommand="python FirebaseCrashH2/src/utils.py &"
    	os.system(CronCommand)
    	print(">>>> Launched Cron Job\n")
        setup_cron_job_completion = True 
    	print(" Clear Flags : setup_cron_job_completion Clear !!!\n")

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
	#print(">>>> Start Cron Job\n")

