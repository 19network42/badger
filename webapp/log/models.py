from django.db import models



class Log(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(unique=True)
