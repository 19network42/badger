from django.contrib import admin
from django.urls import path
from badges.views import add_student, update_student, students

app_name = 'badges'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/', students, name = 'students'),
    path('add_student/', add_student, name = 'add_student'),
    path('update_student/<int:student_id>/', update_student, name = 'update_student'),
]
