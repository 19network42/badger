from django.http import HttpResponse
from badges.models import StudentBadge
from events.models import get_current_event, Mode
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Scan, Log
from badges.models import StudentBadge
import json, sys
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from pages.scans_views import scan_page
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

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
		data_response = response("Tamighi has been scanned... * blushes *", [223, 24, 245], True, mode, len(mode))
	elif login == "Suske":
		data_response = response("Pls tell staff to not reboot me", [204, 255, 204], True, mode, len(mode))
	elif login == "Zeno":
		data_response = response("What is yellow and is waiting?", [153, 0, 153], True, "Default")
	elif login == "skip":
		data_response = response("-> Next", [204, 255, 204], True, mode, len(mode))
	elif login == "ncolin":
		data_response = response("prout", [204, 255, 204], True, mode, len(mode))
	return data_response

@csrf_exempt
def init_page(request):
	if request.method == 'POST':
		event = get_current_event()
		if not (event):
			return HttpResponse("", content_type="application/json", status=404)
		else:
			modes = [mo.type for mo in Mode.objects.all() if mo.event.id == event.id]
			response_data = response("Event init", [0, 0, 255], True, modes, len(modes))
		return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
	return HttpResponse("", content_type="application/json", status=404)


def get_login(scan):
	""" Returns the login of the student owning the badge id passed as parameter """
	student_badge = StudentBadge.objects.filter(badge__uid = scan.uid)
	if len(student_badge) == 0:
		login = "UNDEFINED"
	else:
		login = student_badge[0].student.login
	print("-----------\nGet login result\n----------- : ", login)
	return login

def get_scan(request):
	""" Parse a request from the arduino and returns a corresponding scan object """
	d = json.loads(request.body)
	scan = Scan(uid = d['id'], mode = d['mode'])
	print(str(scan))
	return scan

def scan_limit_reached(scan):
	""" Check if the user reached a consumption limit fir the current mode with its last scan """
	all_scans = Scan.objects.filter(mode = scan.mode, uid = scan.uid, event = scan.event)
	current_mode = Mode.objects.filter(event=scan.event, type=scan.mode)
	if len(all_scans) >= current_mode[0].amount:
		print("-----------\nScan limit reached\n-----------")
		return True
	else:
		return False

@csrf_exempt
def scan(request):
	# POST
	if request.method == 'POST':
		#	Check if there is a current event. Undefined behavior if there is more than one.
		scan = get_scan(request)
		scan.login = get_login(scan)
		
		# Check if there is a current event. Undefined behavior if there is more than one.
		event = get_current_event()
		if not (event):
			response_data = response("No current event.", [255, 0, 0], True, "", 0)
			scan.save()
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=204)
		scan.event = event

		# Check if scan amount is reached for current mode and uid.
		if scan_limit_reached(scan):
			response_data = response("Scan capacity reached.", [255, 0, 0], True, scan.mode, 1)
			scan.save()
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
		#	Else check if uid assigned to StudentBadge
		else :
			scan.validity = True
			if scan.login == "UNDEFINED":
				response_data = response("Badge is not linked to an user", [0, 0, 255], True, scan.mode, 1)
			else:
				response_data = response("Scan ok", [0, 255, 0], True, "Default", 1)
				response_data = specific_response(response_data, scan.login)
		scan.save()
		# Real-time
		log = Log.objects.all()
		real_time_scan(request, scan)
		return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
	# GET
	else:
		return scan_page(request)


def real_time_scan(request, scan):
	channel_layer = get_channel_layer()
	async_convert = async_to_sync(channel_layer.group_send)(
		"log",
		{
			'type' : "send.scan",
			'id' : scan.uid,
			'mode' : scan.mode,
			'login' : scan.login,
			'validity' : scan.validity,
			'event' : scan.event,
		}
		)
	print('test', dir(async_convert))
	#return render(request, "add_event.html") #Pas besoin de ca i guess