from asyncio import events
import re
from django.shortcuts import render
from django.http import HttpResponse
from badges.models import Badge, Student, StudentBadge
from pages.models import Event, get_current_event
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Scan
from pages.models import Event, Mode
from badges.models import StudentBadge
from django.db.models import Q
import json, sys

# Create your views here.


"""
Upon request from the arduino : 
Parse the events in database to find the current one. 
Lists the modes for the event (eg. {'soft', 'water', 'alcool'})
Sends the data back to the arduino under json format.
"""
# def initialize_event(request):
# 	event = get_current_event()
# 	#modes = events.
# 	response_data = {}
# 	for mode in modes:
# 		response_data.append(mode)
# 	return HttpResponse(json.dumps(response_data), content_type="application/json")

def response(msg, led, buzzer, mode):
	response_data = {}
	response_data['msg'] = msg
	response_data['led'] = led
	response_data['buzzer'] = buzzer
	response_data['mode'] = mode
	return response_data


def new_uid(request, uid):
	print(uid)
	context = {
		'error': "uid",
		'scans': Scan.objects.all(),
		'current_scan': Scan.objects.last()
	}
	return render(request, "scans.html", context)


@csrf_exempt
def scan_page(request, *args, **kwargs):
	#Scan.objects.all().delete()
	if request.method == 'POST':
		res = request.body
		d = json.loads(res)
		scan = Scan(uid = d['id'], mode = d['mode'])
		scan.save()

		response_data = response("Badge was scanned", [200, 50, 103], True, "Default")

		student_badge = StudentBadge.objects.filter(badge__uid = scan.uid)
		if len(student_badge) == 0:
			return new_uid(request, scan.uid)

		login = student_badge[0].student.login
		scan.login = login
		scan.save()

		event = get_current_event()
		if not (event):
			response_data = response("No current event", [255, 0, 0], True, "Default")
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=204)
	
		current_mode = Mode.objects.filter(Q(event = event) & Q(type = scan.mode))
		if len(current_mode) == 0:
			response_data = response("No such mode for this event", [255, 0, 0], True, "Default")
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=205)

		scans = Scan.objects.filter(mode = scan.mode, uid = scan.uid, date__range=[event.date, event.end])	
		if len(scans) <= current_mode.amount:
			response_data = response("OK :)", [0, 255, 0], True, "Default")
			print ('gg !!!!!!')
		else :
			response_data = response("NO MORE LEFT :( BYE noob", [255, 0, 0], True, "Default")
			print ('prout')

		print(json.dumps(response_data))

		return HttpResponse(json.dumps(response_data), content_type="application/json", status=100)
	context = {
		'error' : "",
		'scans': Scan.objects.all(),
		'current_scan': Scan.objects.last()
	}
	return render(request, "scans.html", context)

def scan_history(request, *args, **kwargs):
	context = {
		'scans': Scan.objects.all()
	}
	return render(request, "scan.html", context)
