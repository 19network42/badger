from django.db import models
from django.utils import timezone
from badges.models import Badge, StudentBadge
from events.models import Event

class Log(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)

class Scan(models.Model):

	uid = models.CharField(max_length=15)
	date = models.DateTimeField(default=timezone.now)
	mode = models.CharField(max_length=15)
	login = models.CharField(max_length=15)
	validity = models.BooleanField(default=False)
	event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)


	def __str__(self):
		return "Scan_" + self.uid + "_" + self.date.strftime('%m/%d/%y %H:%M')