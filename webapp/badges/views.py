from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Student, Badge, StudentBadge
from .forms import StudentForm, ScanForm
from accounts import urls
from accounts.models import User
import json
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .tasks import update_students
from api.models import Scan

@login_required(login_url='accounts:login')
def	add_student(request):
	submitted = False
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/students?submitted=True')
			# return HttpResponseRedirect('/add_student?submitted=True')
	else:
		form = StudentForm()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, "add_student.html", {'form': form, 'submitted': submitted})

@login_required(login_url='accounts:login')
def	update_student(request, student_id):
	student = Student.objects.get(pk=student_id)
	form = StudentForm(request.POST or None, instance=student)
	if form.is_valid():
		form.save()
		return redirect('badges:students')
	return render(request, "update_student.html", {'student': student, 'form': form})

@login_required(login_url='accounts:login')
def	one_student(request, student_id, *args, **kwargs):
	student = Student.objects.get(pk=student_id)
	context = {
		'student' : student,
	}
	return render(request, "one_student.html", context)

@login_required(login_url='accounts:login')
def testing_student(request):
	update_students()
	return HttpResponse(str(update_students()))
from badges.models import Student

@login_required(login_url='accounts:login')
def list_student(request):
	context = {
		'students': Student.objects.all(),
	}
	return render(request, "students.html", context)

def update_studentbadge(request, scan_id):
	scan = Scan.objects.get(pk=scan_id)
	form = ScanForm(request.POST or None, instance=scan)
	if request.method == "POST":
		form.save()
		return redirect('badges:scan')
	context = {
		'scan': scan,
		'form': form,
	}
	return render(request, "update_studentbadge.html", context)
