from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Badge, StudentBadge
from .forms import StudentForm
from accounts.models import User
import json
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .tasks import update_students

def	students(request, *args, **kwargs):
	context = {
		'students': Student.objects.all(),
	}
	return render(request, "students.html", context)

def	add_student(request):
	submitted = False
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_student?submitted=True')
	else:
		form = StudentForm()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, "add_student.html", {'form': form, 'submitted': submitted})

def	update_student(request, student_id):
	student = Student.objects.get(pk=student_id)
	form = StudentForm(request.POST or None, instance=student)
	if form.is_valid():
		form.save()
		return redirect('badges:students')
	return render(request, "update_student.html", {'student': student, 'form': form})

def	one_student(request, student_id, *args, **kwargs):
	student = Student.objects.get(pk=student_id)
	context = {
		'student' : student,
	}
	return render(request, "one_event.html", context)

# Create your views her
def testing_student(request):
	update_students()
	return HttpResponse("tested")
