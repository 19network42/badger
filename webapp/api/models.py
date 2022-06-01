from django.db import models
from django.utils import timezone
from badges.models import Badge, StudentBadge
# Create your models here.
class Scan(models.Model):
	uid = models.CharField(max_length=15)
	date = models.DateTimeField(default=timezone.now)
	mode = models.CharField(max_length=15)
	login = models.CharField(max_length=15)

	def find_badge(self):
		badges = StudentBadge.objects.all()
		for badge in badges:
			if badge.badge.uid == self.uid:
				return badge
		return None

	def __str__(self):
		return "Scan_" + self.uid + "_" + self.date.strftime('%m/%d/%y %H:%M')