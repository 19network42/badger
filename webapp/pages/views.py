from django.shortcuts import render
from django.db import models
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Event, Mode
from .forms import EventForm, ModeForm
from .utils import Calendar
from badges.models import Student, StudentBadge, Badge
from badges.forms import StudentForm
from accounts.models import User
import json
import calendar
import time
from calendar import HTMLCalendar
from datetime import datetime, timedelta, date
from api.models import Scan
from django.utils.safestring import mark_safe
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe



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
def user_page():
	context = {
		'users': User.objects.all(),
	}
	return render(request, "user.html", context)

def conso_page(request, event_id):
	event = Event.objects.get(pk=event_id)
	conso = [co for co in Mode.objects.all() if co.event.id == event_id],
	context = {
		'scans' : [scan for scan in Scan.objects.all() if event.date < scan.date < event.end],
		'event' : event
	}

#-----------------------------------#
#									#
#				PAGES				#
#									#
#-----------------------------------#
#credits to Hui Wen https://github.com/huiwenhw


class CalendarView(generic.ListView):
	model = Event
	template_name = 'calendar.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		d = get_date(self.request.GET.get('month', None))

		# Instantiate our calendar class with today's year and date
		cal = Calendar(d.year, d.month)

		# Call the formatmonth method, which returns our calendar as a table
		html_cal = cal.formatmonth(withyear=True)
		context['calendar'] = mark_safe(html_cal)
		context['prev_month'] = prev_month(d)
		context['next_month'] = next_month(d)
		return context

def prev_month(d):
	first = d.replace(day=1)
	prev_month = first - timedelta(days=1)
	month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
	return month

def next_month(d):
	days_in_month = calendar.monthrange(d.year, d.month)[1]
	last = d.replace(day=days_in_month)
	next_month = last + timedelta(days=1)
	month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
	return month

def get_date(req_day):
	if req_day:
		year, month = (int(x) for x in req_day.split('-'))
		return date(year, month, day=1)
	return datetime.today()

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
