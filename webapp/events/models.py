from django.db import models
from django.utils import timezone
from datetime import datetime
from django.urls import reverse

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
	@property
	def get_html_url(self):
		url = reverse('events:one_event', args=(self.id,))
		return f'<a href="{url}"> {self.name} </a>'
	def __str__(self):
		return self.name

def	get_current_event():
	events = []
	for ev in Event.objects.all():
		if ev.is_current():
			events.append(ev)
	if len(events) > 0:
		return events[0]

class Mode(models.Model):
	amount = models.IntegerField(null=True, blank=True)
	type = models.CharField(max_length=100, null=True, blank=True)
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event', null=True)

	def __str__(self):
		return "[" + str(self.event) + "] " +   str(self.amount)  + " " + self.type