from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
	list_display = ('login', 'displayname', 'user_id', 'is_staff')
admin.site.register(User, UserAdmin)