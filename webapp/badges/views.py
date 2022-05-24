from django.http import HttpResponse
from django.shortcuts import render
from .tasks import update_students
# Create your views here.
def testing_student(request):
    update_students()
    return HttpResponse("tested")
