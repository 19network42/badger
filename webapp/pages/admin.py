from django.contrib import admin
from .models import Scan, Event, Mode

# Register your models here.
admin.site.register(Scan)
admin.site.register(Event)
admin.site.register(Mode)