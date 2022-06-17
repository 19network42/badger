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

@login_required(login_url='pages:login')
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
	return render(request, "add_student.html", {'form': form, 'submitted': submitted})


@login_required(login_url='pages:login')
def	update_student(request, student_id):
	student_bg = StudentBadge.objects.get(pk=student_id)
	form = StudentBadgeForm(request.POST or None, instance=student_bg)
	if form.is_valid():
		form.save()
		# return redirect('badges:one_student', student_id=student_id)
		return redirect('badges:students')
	return render(request, "update_student.html", {'student_bg': student_bg, 'form': form})


@login_required(login_url='pages:login')
def	one_student(request, student_id, *args, **kwargs):
	student_bg = StudentBadge.objects.get(pk=student_id)
	context = {
		'student_bg' : student_bg,
	}
	return render(request, "one_student.html", context)


@login_required(login_url='pages:login')
def testing_student(request):
	update_students()
	return HttpResponse(str(update_students()))


@login_required(login_url='pages:login')
def list_student(request):
	context = {
		'student_bgs': StudentBadge.objects.all(),
	}
	return render(request, "students.html", context)


def update_studentbadge(request, scan_id):
	scan = Scan.objects.get(pk=scan_id)
	form = ScanForm(request.POST or None, instance=scan)
	error = ""
	if request.method == "POST":
		form.save()
		student_badge = StudentBadge.objects.filter(student__login=form.instance.login)
		if len(student_badge) == 0:
			error = "Login not found"
		elif student_badge[0].badge.uid != None:
			error = "Login is already assigned uid"
		else:
			student_badge[0].badge.uid = form.instance.uid
			student_badge[0].badge.save()
			return redirect('api:scan')
		form.instance.login = "UNDEFINED"
		form.save()
	context = {
		'form': form,
		'error':error,
	}
	return render(request, "update_studentbadge.html", context)
