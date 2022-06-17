from django.contrib import admin
from .models import Scan, Event

# Register your models here.
admin.site.register(Scan)
admin.site.register(Event)