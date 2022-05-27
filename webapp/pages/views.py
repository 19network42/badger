from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Event, Mode
from .forms import EventForm, ModelForm
from badges.models import Student
from badges.forms import StudentForm
from accounts.models import User
import json
import calendar
from calendar import HTMLCalendar
from datetime import datetime



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
		students = Student.objects.filter(Q(login=searched) | Q(displayname__contains=searched))
		return render(request, 'search_general.html', 
			{'searched': searched, 'events': events, 'students': students})
	else:
		return render(request, 'search_general.html', {})

@login_required(login_url='accounts:login')
def update_mode(request, event_id):
	event = Event.objects.get(pk=event_id)
	mode_form = ModeForm()

	if mode_form.is_valid():
		mode_form.save()
		return redirect('pages:events/<int:event_id>/')
	context = {
		'event': event,
		'modes' : [mo for mo in Mode.objects.all() if mo.event.id == event_id],
		'mode_form': mode_form
	}
	return render(request, "update_mode.html", context)

@login_required(login_url='accounts:login')
def	update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	event_form = EventForm(request.POST or None, instance=event)
	if event_form.is_valid():
		event_form.save()
		return redirect('pages:events')
	context = {
		'event': event,
		'event_form': event_form,
	}
	return render(request, "update_event.html", context)

@login_required(login_url='accounts:login')
def	add_event(request):
	submitted = False
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add_event?submitted=True')
	else:
		form = EventForm()
		if 'submitted' in request.GET:
			submitted = True
	return render(request, "add_event.html", {'form': form, 'submitted': submitted})
