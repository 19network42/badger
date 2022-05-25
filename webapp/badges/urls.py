from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
from badges.views import add_student, update_student, students
=======
from badges.views import testing_student
>>>>>>> 8ce54b259d19077bd9cf0a06647b73af453d20ff

app_name = 'badges'

urlpatterns = [
<<<<<<< HEAD
    path('admin/', admin.site.urls),
    path('students/', students, name = 'students'),
    path('add_student/', add_student, name = 'add_student'),
    path('update_student/<int:student_id>/', update_student, name = 'update_student'),
=======
    path('test_student/', testing_student, name = 'test_student')
>>>>>>> 8ce54b259d19077bd9cf0a06647b73af453d20ff
]
