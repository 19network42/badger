from django.db import models
from django.utils import timezone
from datetime import datetime
import zoneinfo
import time
import pytz

utc=pytz.UTC

class Event(models.Model):
	date = models.DateTimeField(default=timezone)
	drinks = models.CharField(max_length = 2)
	name = models.CharField(max_length = 100)
	end = models.DateTimeField()
	print(date)

	def	is_current(self):
		now = datetime.now()
		now = utc.localize(now)
		return (self.date < now < self.end)

class Scan(models.Model):
	uid = models.CharField(max_length=15)
	date = models.DateTimeField(default=timezone.now)
