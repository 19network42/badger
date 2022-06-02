from django.contrib import admin
from django.urls import path
from badges.views import (
							add_student,
							update_student,
							testing_student,
							one_student,
							list_student,
						)

app_name = 'badges'

urlpatterns = [
	path('admin/', admin.site.urls),
	path('add_student/', add_student, name = 'add_student'),
	path('update_student/<int:student_id>/', update_student, name = 'update_student'),
	path('test_student/', testing_student, name = 'test_student'),
	path('students/<int:student_id>/', one_student, name = 'one_student'),
	path('students/', list_student, name = 'students'),
]
