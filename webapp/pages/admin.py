from django.contrib import admin
from .models import Scan, Event, Mode, Type, Amount

# Register your models here.
admin.site.register(Scan)
admin.site.register(Event)
admin.site.register(Mode)
admin.site.register(Type)
admin.site.register(Amount)