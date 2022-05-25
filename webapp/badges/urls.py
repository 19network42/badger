from django.urls import path
from badges.views import testing_student, list_student

app_name = 'badges'

urlpatterns = [
    path('test_student/', testing_student, name = 'test_student'),
    path('student_list/', list_student, name = 'test_student')
]
