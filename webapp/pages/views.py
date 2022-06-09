from django.shortcuts import render
from django.db import models
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Event, Mode
from .forms import EventForm, ModeForm
from badges.models import Student, StudentBadge, Badge
from badges.forms import StudentForm
from accounts.models import User
import json
import calendar
import time
from calendar import HTMLCalendar
from datetime import datetime
from api.models import Scan


#-----------------------------------#
#									#
#				PAGES				#
#									#
#-----------------------------------#

@csrf_exempt
def	home_page(request, *args, **kwargs):
	context = {
		'events' : [ev for ev in Event.objects.all() if ev.is_current()]
	}
	return render(request, "home.html", context)

@csrf_exempt
@login_required(login_url='accounts:login')
def events_page(request, *args, **kwargs):
	if request.method == 'POST':
		res = request.body
		d = json.loads(res)

	context = {
		'events': Event.objects.all(),
	}
	return render(request, "events.html", context)

@login_required(login_url='accounts:login')
@csrf_exempt
def	one_event(request, event_id, *args, **kwargs):
	event = Event.objects.get(pk=event_id)
	context = {
		'scans' : [sca for sca in Scan.objects.all() if event.date < sca.date < event.end ],
		'modes' : [mo for mo in Mode.objects.all() if mo.event.id == event_id],
		'event' : event
	}
	return render(request, "one_event.html", context)

@login_required(login_url='accounts:login')
@csrf_exempt
def user_page(request, *args, **kwargs):
	context = {
		'users': User.objects.all(),
	}
	return render(request, "user.html", context)

def	calendar_page(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	month = month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)
	cal = HTMLCalendar().formatmonth(year, month_number)
	now = datetime.now()
	current_year = now.year
	time = now.strftime('%H:%M %p')
	day = now.strftime('%j')
	return render(request, 'calendar.html', {"year": year, "month": month,
		"month_number": month_number, "cal": cal, "now": now, 
		"current_year": current_year, "time": time, "day": day})

# def	calendar_page(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
# 	month = month.capitalize()
# 	month_number = list(calendar.month_name).index(month)
# 	month_number = int(month_number)
# 	cal = HTMLCalendar().formatmonth(year, month_number)
# 	now = datetime.now()
# 	current_year = now.year
# 	time = now.strftime('%H:%M %p')
# 	day = now.strftime('%j')
# 	return render(request, 'calendar.html', {"year": year, "month": month,
# 		"month_number": month_number, "cal": cal, "now": now, 
# 		"current_year": current_year, "time": time, "day": day})

# def conso_page(request, event_id):
# 	event = Event.objects.get(pk=event_id)
# 	conso = [co for co in Mode.objects.all() if co.event.id == event_id],
# 	context = {
# 		'scans' : [scan for scan in Scan.objects.all() if event.date < scan.date < event.end],
# 		'event' : event
# 	}

#-----------------------------------#
#			SEARCH					#
#				UPDATE				#
#					ADD	EVENT		#
#-----------------------------------#

@login_required(login_url='accounts:login')
@csrf_exempt
def	search_general(request):
	if request.method == "POST":
		searched = request.POST['searched']
		events = Event.objects.filter(name__contains=searched)
		student_bgs = StudentBadge.objects.filter(Q(student__login__contains=searched) | Q(student__displayname__contains=searched))
		return render(request, 'search_general.html', 
			{'searched': searched, 'events': events, 'student_bgs': student_bgs})
	else:
		return render(request, 'search_general.html', {})

def mode_page(request, event, context):
	mode_form = ModeForm(request.POST or None)
	error = ""
	mode_form.instance.event = event

	if request.method == "POST":
		action = request.POST.get("action")
		delete = request.POST.get("delete")

		if action == "add":
			mode_form.save()
			if mode_form.instance.type in [mo.type for mo in Mode.objects.filter(event=event) if mo != mode_form.instance]:
				error = "Already exist"
				mode_form.instance.delete()
			if mode_form.instance.type == "" or mode_form.instance.amount == None:
				error = "Fill out mode field"
				mode_form.instance.delete()
		if delete:
			Mode.objects.filter(id=delete).delete()

	context['modes'] = [mo for mo in Mode.objects.all() if mo.event == event]
	context['mode_form'] = mode_form
	context['mode_error'] = error

@login_required(login_url='accounts:login')
def	update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	event_form = EventForm(request.POST or None, instance=event)

	if request.method == "POST":
		submit = request.POST.get("submit")		
		if submit == "submitted":
			event_form.save()
			return redirect('pages:events')
	
	context = {
	'event': event,
	'event_form': event_form,
	}
	mode_page(request, event, context)

	return render(request, "update_event.html", context)

@login_required(login_url='accounts:login')
def	add_event(request):
	form = EventForm(request.POST or None)

	if request.method == "POST":
		submit = request.POST.get("submit")
		form.save()
		if submit == "first":
			return HttpResponseRedirect('/update_event/' + str(form.instance.id))

	context = {
		'form': form,
	}
	return render(request, "add_event.html", context)

@login_required(login_url='accounts:login')
def	delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.method == "POST":
		event.delete()
		return redirect('pages:events')
	return render(request, 'delete_event.html', {'event': event})
