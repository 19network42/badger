from django.http import HttpResponse
from django.shortcuts import render
from .tasks import update_students
from badges.models import Student
# Create your views here.
def testing_student(request):
    test = update_students()
    return HttpResponse(str(test))

def list_student(request):
    context = {
		'students': Student.objects.all(),
	}
    return render(request, "student.html", context)