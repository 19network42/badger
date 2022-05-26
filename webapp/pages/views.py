from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event
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
def events_page(request, *args, **kwargs):
	if request.method == 'POST':
		res = request.body
		d = json.loads(res)

	context = {
		'events': Event.objects.all(),
	}
	return render(request, "events.html", context)

def	one_event(request, event_id, *args, **kwargs):
	one_event = Event.objects.get(id=event_id)
	print(one_event)
	context = {
		'one_event' : one_event,
	}
	return render(request, "one_event.html", context)

def user_page(request, *args, **kwargs):
	context = {
		'users': User.objects.all(),
	}
	return render(request, "user.html", context)



def	search_general(request):
	if request.method == "POST":
		searched = request.POST['searched']
		events = Event.objects.filter(name__contains=searched)
		#users = Scan.objects.filter(uid__contains=searched)
		return render(request, 'search_general.html', {'searched': searched, 'events': events, 'users': users})
	else:
		return render(request, 'search_general.html', {})

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
		"month_number": month_number, "cal": cal, "now": now, "current_year": current_year,
		"time": time, "day": day})
