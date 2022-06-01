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

@csrf_exempt
def scan_page(request, *args, **kwargs):
	#Scan.objects.all().delete()
	if request.method == 'POST':
		res = request.body
		d = json.loads(res)
		scan = Scan(uid = d['id'], mode = d['mode'])
		scan.save()

		response_data = {}
		response_data['msg'] = "Badge was scanned"
		response_data['led'] = [200, 50, 103]
		response_data['buzzer'] = True
		response_data['mode'] = "Default"

		badge = Badge.objects.get(uid = scan.uid)
		if not (badge):
			response_data['msg'] = "Scan error"
			response_data['led'] = [255, 0, 0]
			response_data['buzzer'] = True
			response_data['mode'] = "Default"
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=1)

		student = StudentBadge.objects.get(badge = badge)
		if not (student):
			response_data['msg'] = "Scan error"
			response_data['led'] = [255, 0, 0]
			response_data['buzzer'] = True
			response_data['mode'] = "Default"
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=101)

		event = get_current_event()
		if not (event):
			response_data['msg'] = "No current event"
			response_data['led'] = [255, 0, 0]
			response_data['buzzer'] = True
			response_data['mode'] = "Default"
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=204)
		
		current_mode = Mode.objects.filter(Q(event = event) & Q(type = scan.mode))
		if not (current_mode):
			response_data['msg'] = "No such mode for this event"
			response_data['led'] = [255, 0, 0]
			response_data['buzzer'] = True
			response_data['mode'] = "Default"
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=205)
		scans = Scan.objects.filter(mode = scan.mode, uid = scan.uid, date__range=[event.date, event.end])
		
		# if len(scans) <= current_mode.amount:
		# 	print ('gg !!!!!!')
		# else :
		# 	print ('prout')

		print(json.dumps(response_data))

		return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
	context = {
		'scans': Scan.objects.all(),
		'current_scan': Scan.objects.last()
	}
	return render(request, "scans.html", context)

def scan_history(request, *args, **kwargs):
	context = {
		'scans': Scan.objects.all()
	}
	return render(request, "scan.html", context)
