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
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

"""
Upon request from the arduino : 
Parse the events in database to find the current one. 
Lists the modes for the event (eg. {'soft', 'water', 'alcool'})
Sends the data back to the arduino under json format.
"""

def response(msg, led, buzzer, mode, mode_amount):
	response_data = {}
	response_data['msg'] = msg
	response_data['led'] = led
	response_data['buzzer'] = buzzer
	response_data['mode'] = mode
	response_data['mode_amount'] = mode_amount 
	return response_data

def specific_response(data_response, login):
	mode = ['default']
	if login == "tamighi":
		data_response = response("Lord Tamighi has been scanned... * blushes *", [223, 24, 245], True, mode, len(mode))
	elif login == "zeno":
		data_response = response("* insert funny joke here *", [153, 0, 153], True, mode, len(mode))
	elif login == "Suske":
		data_response = response("Pls tell staff to not reboot me", [204, 255, 204], True, mode, len(mode))
	elif login == "skip":
		data_response = response("-> Next", [204, 255, 204], True, mode, len(mode))
	elif login == "archimède":
		data_response = response("scan .. for ..* PANIC *", [255, 128, 0], True, mode, len(mode))
	return data_response


@csrf_exempt
def init_page(request, *args, **kwargs):
	if request.method == 'POST':
		event = get_current_event()
		if not (event):
			return HttpResponse("", content_type="application/json", status=404)
		else:
			modes = [mo.type for mo in Mode.objects.all() if mo.event.id == event.id]
			response_data = response("Event init", [0, 0, 255], True, modes, len(modes))
		return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
	return HttpResponse("", content_type="application/json", status=404)
	
@csrf_exempt
def scan_page(request, *args, **kwargs):

	#	POST management
	if request.method == 'POST':
		res = request.body
		print(res)
		d = json.loads(res)
		scan = Scan(uid = d['id'], mode = d['mode'])
		test_scan(request, scan)
		#	Assign a login to the scan if the uid is already assigned. Login is set as "UNDEFINED" if not.
		student_badge = StudentBadge.objects.filter(badge__uid = scan.uid)
		if len(student_badge) == 0:
			login = "UNDEFINED"
		else:
			login = student_badge[0].student.login
		scan.login = login
	
		#	Check if there is a current event. Undefined behavior if there is more than one.
		event = get_current_event()
		if not (event):
			response_data = response("No current event.", [255, 0, 0], True, "Default", 0)
			scan.save()
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=204)

		scan.event = event

		#	Undefined behavior if the mode is invalid.
	
		#	Check if scan amount is reached for current mode and uid.
		all_scans = Scan.objects.filter(mode = scan.mode, uid = scan.uid, event = scan.event)
		current_mode = Mode.objects.filter(event=event, type=scan.mode)	

		if len(all_scans) >= current_mode[0].amount:
			response_data = response("Scan capacity reached.", [255, 0, 0], True, "Default", 1)
			scan.save()
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=205)

		#	Else check if uid assigned to StudentBadge
		else :
			scan.validity = True
			student_badge = StudentBadge.objects.filter(badge__uid = scan.uid)
			if login == "UNDEFINED":
				response_data = response("Badge is not linked to an user", [0, 0, 255], True, "Default", 1)
			else:
				response_data = response("Scan ok", [0, 255, 0], True, "Default", 1)

				#	Modify response message if specific login (Please do not remove this line!)
				response_data = specific_response(response_data, login)
		
		scan.save()
		return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
	#	GET management
	context = {
		'scans': Scan.objects.all(),
		'current_scan': Scan.objects.last()
	}
	return render(request, "scans.html", context)

def test_scan(request, scan):
	channel_layer = get_channel_layer()
	blabla = async_to_sync(channel_layer.group_send)(
		"log",
		{
			'type' : "send.scan",
			'id' : scan.uid,
			'mode' : scan.mode,
		}
		)
	print('test', dir(blabla))
	return render(request, "add_event.html")


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
