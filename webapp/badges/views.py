from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from badges.models import StudentBadge
from badges.forms import StudentBadgeForm
from api.forms import ScanForm
from badges.tasks import update_students
from api.models import Scan

#---------------------------------------#
#										#
#				BADGES					#
#										#
#---------------------------------------#

@login_required(login_url='accounts:login')
def	add_student(request):
	submitted = False
	if request.method == "POST":
		form = StudentBadgeForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/students')
	else:
		form = StudentBadgeForm()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, "badges/add_student.html", {'form': form, 'submitted': submitted})


@login_required(login_url='accounts:login')
def	update_student(request, student_id):
	student_bg = StudentBadge.objects.get(pk=student_id)
	form = StudentBadgeForm(request.POST or None, instance=student_bg)
	if form.is_valid():
		form.save()
		return redirect('badges:students')
	return render(request, "badges/update_student.html", {'student_bg': student_bg, 'form': form})


@login_required(login_url='accounts:login')
def	one_student(request, student_id):
	student_bg = StudentBadge.objects.get(pk=student_id)
	context = {
		'student_bg' : student_bg,
	}
	return render(request, "badges/one_student.html", context)


@login_required(login_url='accounts:login')
def testing_student(request):
	update_students()
	return HttpResponse(str(update_students()))


@login_required(login_url='accounts:login')
def list_student(request):
	context = {
		'student_bgs': StudentBadge.objects.all(),
	}
	return render(request, "badges/students.html", context)


def update_studentbadge(request, scan_id):
	scan = Scan.objects.get(pk=scan_id)
	form = ScanForm(request.POST or None, instance=scan)
	error = ""

	if request.method == "POST":
		form.save()
		student_badge = StudentBadge.objects.filter(student__login=form.instance.login)

		#	Error management
		if len(student_badge) == 0:
			error = "Login not found"
		elif student_badge[0].badge.uid != None and student_badge[0].badge.uid != form.instance.uid:
			error = "Login is already assigned uid"
	
		#	The student badge is correct and the uid is assigned to it.
		else:
			student_badge[0].badge.uid = form.instance.uid
			student_badge[0].badge.save()
			return redirect('general:scans')
		
		#	If there is an error, login is undefined or set back to its original state,
		#	error is set and render studentbadge.html

		login = StudentBadge.objects.filter(badge__uid=form.instance.uid)
		if len(login) != 0:
			form.instance.login = login[0].student.login
		else:
			form.instance.login = "UNDEFINED"
		form.save()
		
	context = {
		'form': form,
		'error':error,
	}
	return render(request, "badges/update_studentbadge.html", context)
