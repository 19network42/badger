from asyncio import events
import re
from django.shortcuts import redirect, render
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

"""
Upon request from the arduino : 
Parse the events in database to find the current one. 
Lists the modes for the event (eg. {'soft', 'water', 'alcool'})
Sends the data back to the arduino under json format.
"""

def response(msg, led, buzzer, mode):
	response_data = {}
	response_data['msg'] = msg
	response_data['led'] = led
	response_data['buzzer'] = buzzer
	response_data['mode'] = mode
	return response_data

def specific_response(data_response, login):
	if login == "tamighi":
		data_response = response("Lord Tamighi has been scanned... * blushes *", [223, 24, 245], True, "Default")
	elif login == "zeno":
		data_response = response("* insert funny joke here *", [153, 0, 153], True, "Default")
	elif login == "Suske":
		data_response = response("Pls tell staff to not reboot me", [204, 255, 204], True, "Default")
	elif login == "skip":
		data_response = response("-> Next", [204, 255, 204], True, "Default")
	elif login == "archimède":
		data_response = response("scan .. for ..* PANIC *", [255, 128, 0], True, "Default")
	return data_response


# def initialize_event(request):
# 	event = get_current_event()
# 	#modes = events.
# 	response_data = {}
# 	for mode in modes:
# 		response_data.append(mode)
# 	return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def scan_page(request, *args, **kwargs):
	if request.method == 'POST':
		res = request.body
		d = json.loads(res)
		scan = Scan(uid = d['id'], mode = d['mode'])

		#	Define login for scanned badge.
		student_badge = StudentBadge.objects.filter(badge__uid = scan.uid)
		if len(student_badge) == 0:
			login = "UNDEFINED"
		else:
			login = student_badge[0].student.login
		scan.login = login
		scan.save()

		#	Check if current event.
		event = get_current_event()
		if not (event):
			response_data = response("No current event.", [255, 0, 0], True, "Default")
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=204)

		#	Check if mode sent is in event.
		current_mode = Mode.objects.filter(Q(event = event) & Q(type = scan.mode))
		if len(current_mode) == 0:
			response_data = response("No such mode for this event.", [255, 0, 0], True, "Default")
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=205)
	
		#	Check if scan amount is reached for current mode and uid.
		scans = Scan.objects.filter(mode = scan.mode, uid = scan.uid, date__range=[event.date, event.end])
	
		if len(scans) > current_mode[0].amount:
			response_data = response("Scan capacity reached", [255, 0, 0], True, "Default")
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=205)

		scans = Scan.objects.filter(mode = scan.mode, uid = scan.uid, date__range=[event.date, event.end])
		if len(scans) <= current_mode.amount:
			response_data = response("OK :)", [0, 255, 0], True, "Default")
			print ('gg !!!!!!')
		else :
			student_badge = StudentBadge.objects.filter(badge__uid = scan.uid)
			if login == "UNDEFINED":
				response_data = response("Badge is not linked to an user", [0, 0, 255], True, "Default")
			else:
				response_data = response("Scan ok", [0, 255, 0], True, "Default")

				#	Modify response message if specific login (Please do not remove this line!)
				response_data = specific_response(response_data, login)

		return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
	
	#	GET page here
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

@login_required(login_url='accounts:login')
def	delete_scan(request, scan_id):
	scan = Scan.objects.get(pk=scan_id)
	if request.method == "POST":
		scan.delete()
		return redirect('api:scan')
	return render(request, 'delete_event.html', {'scan': scan})
