from django.contrib import admin
from .models import Student, Badge, StudentBadge


class StudentAdmin(admin.ModelAdmin):
    list_display = ('login', 'displayname', 'intra_id', 'is_staff')


admin.site.register(Student, StudentAdmin)


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('serial', 'uid', 'reference', 'badge_type', 'lost')


admin.site.register(Badge, BadgeAdmin)


class StudentBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'start_at', 'end_at')


admin.site.register(StudentBadge, StudentBadgeAdmin)
