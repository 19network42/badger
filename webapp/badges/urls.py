from django.urls import path
from badges.views import testing_student

app_name = 'badges'

urlpatterns = [
    path('test_student/', testing_student, name = 'test_student')
]
