from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Student, Badge, StudentBadge
from .forms import StudentForm, StudentBadgeForm
from accounts import urls
from accounts.models import User
import json
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .tasks import update_students

@login_required(login_url='accounts:login')
def	add_student(request):
	submitted = False
	if request.method == "POST":
		form = StudentBadgeForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/students?submitted=True')
			# return HttpResponseRedirect('/add_student?submitted=True')
	else:
		form = StudentBadgeForm()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, "add_student.html", {'form': form, 'submitted': submitted})

@login_required(login_url='accounts:login')
def	update_student(request, student_id):
	student_bg = StudentBadge.objects.get(pk=student_id)
	form = StudentBadgeForm(request.POST or None, instance=student_bg)
	if form.is_valid():
		form.save()
		# return redirect('badges:one_student', student_id=student_id)
		return redirect('badges:students')
	return render(request, "update_student.html", {'student_bg': student_bg, 'form': form})

@login_required(login_url='accounts:login')
def	one_student(request, student_id, *args, **kwargs):
	student_bg = StudentBadge.objects.get(pk=student_id)
	context = {
		'student_bg' : student_bg,
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
		'student_bgs': StudentBadge.objects.all(),
	}
	return render(request, "students.html", context)
