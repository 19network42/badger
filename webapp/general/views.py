from events.models import Event, get_current_event, Mode
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from api.models import Scan
from events.models import Event
from badges.models import StudentBadge
from django.db.models import Q
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from calendar import HTMLCalendar
from datetime import datetime, timedelta, date


#---------------------------------------#
#										#
#				CALENDAR				#
#										#
#---------------------------------------#
#credits to Hui Wen https://github.com/huiwenhw


class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		today = datetime.now()
		events_per_day = events.filter(date__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'
		if day != 0:
			if today.day == day:
				return f"<td><span class='today'>{day}</span><ul> {d} </ul></td>"
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return "<td></td>"

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(date__year=self.year, date__month=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
		cal += f"{self.formatweekheader()}\n"
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f"{self.formatweek(week, events)}\n"
		return cal


class CalendarView(generic.ListView):
	model = Event
	template_name = 'general/calendar.html'

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


#---------------------------------------#
#										#
#				GENERAL					#
#										#
#---------------------------------------#


@csrf_exempt
def	home_page(request, *args, **kwargs):
	return render(request, "general/home.html")


@login_required(login_url='accounts:login')
@csrf_exempt
def	search_general(request):
	if request.method == "POST":
		searched = request.POST['searched']
		events = Event.objects.filter(name__contains=searched)
		student_bgs = StudentBadge.objects.filter(Q(student__login__contains=searched) | Q(student__displayname__contains=searched))
		return render(request, 'general/search_general.html', 
			{'searched': searched, 'events': events, 'student_bgs': student_bgs})


#---------------------------------------#
#										#
#				SCAN					#
#										#
#---------------------------------------#


@csrf_exempt
def	scan_page(request):
	#	GET management
	context = {
		'scans': Scan.objects.all(),
		'current_scan': Scan.objects.last()
	}
	return render(request, "general/scans.html", context)

def search_scan_page(request):
	if request.method == 'GET':
		return render(request, "general/search_scans.html", {})

	login = request.POST.get("login")
	event_name = request.POST.get("event")
	scans = Scan.objects.all()
	if event_name:
		event = event.last()
	else:
		event = None

	event = Event.objects.filter(name = event_name)
	if event:
		scans = scans.filter(event = event)
	if login:
		scans = scans.filter(login = login)

	context = {
		'scans': scans,
		'current_scan': scans.last()
	}
	return render(request, "general/scans.html", context)

@login_required(login_url='accounts:login')
def	delete_scan(request, scan_id):
	scan = Scan.objects.get(pk=scan_id)
	if request.method == "POST":
		scan.delete()
		return redirect('general:scan')
	return render(request, 'events/delete_event.html', {'scan': scan})
