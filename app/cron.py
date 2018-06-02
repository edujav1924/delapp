import os
from django.core import management
from django.conf import settings
def my_scheduled_job():
  management.call_command('dbbackup')
