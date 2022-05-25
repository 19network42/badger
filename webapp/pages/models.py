from plistlib import UID
from django.db import models
from django.utils import timezone
from datetime import datetime

def two_hours_hence():
	return timezone.now() + timezone.timedelta(hours=1)

class Type(models.Model):
	type = models.CharField(max_length = 100)
	def __str__(self):
		return str(self.type)

class Amount(models.Model):
	amount = models.IntegerField()
	def __str__(self):
		return str(self.amount)

class Mode(models.Model):
	amount = models.IntegerField()
	type = models.ForeignKey(Type, on_delete=models.CASCADE)

class Event(models.Model):
	date = models.DateTimeField(default=timezone.now)
	name = models.CharField(max_length = 100)
	end = models.DateTimeField(default=two_hours_hence)
	mode = models.ManyToManyField(Mode)

	def is_current(self):
		now = datetime.now()
		return (self.date < now < self.end)

class Scan(models.Model):
	uid = models.CharField(max_length=15)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "Scan_" + self.uid + "_" + self.date.strftime('%m/%d/%y %H:%M')
