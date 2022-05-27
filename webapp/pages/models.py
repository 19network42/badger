from asyncio import events
from plistlib import UID
from django.db import models
from django.utils import timezone
from datetime import datetime

#Quick fix for dealing with timezone difference.. should probably find a better solution 
def two_hours_hence():
	return timezone.now() + timezone.timedelta(hours=1)


class Event(models.Model):
	date = models.DateTimeField(default=timezone.now)
	name = models.CharField(max_length = 100)
	end = models.DateTimeField(default=two_hours_hence)
	def is_current(self):
		now = datetime.now()
		return (self.date < now < self.end)

def	get_current_event():
	events = []
	for ev in Event.objects.all():
		if ev.is_current():
			events.append(ev)
	# Should we prioritize one event over another if two events overlap?
	# How do we handle this ?
	if len(events) > 1:
		print("Error, multiple events found")
	return events[0]

class Mode(models.Model):
	amount = models.IntegerField()
	type = models.CharField(max_length=100)
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event')

class Scan(models.Model):
	uid = models.CharField(max_length=15)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "Scan_" + self.uid + "_" + self.date.strftime('%m/%d/%y %H:%M')
