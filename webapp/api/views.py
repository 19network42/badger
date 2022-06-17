from django.http import HttpResponse
from badges.models import StudentBadge
from events.models import get_current_event, Mode
from django.views.decorators.csrf import csrf_exempt
from .models import Scan
from badges.models import StudentBadge
import json
from pages.scans_views import scan_page

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
	elif login == "Zeno":
		data_response = response("What is yellow and is waiting?", [153, 0, 153], True, "Default")
	elif login == "skip":
		data_response = response("-> Next", [204, 255, 204], True, "Default")
	elif login == "archimède":
		data_response = response("scan .. for ..* PANIC *", [255, 128, 0], True, "Default")
	return data_response

@csrf_exempt
def init_page(request):
	if request.method == 'POST':
		event = get_current_event()
		if not (event):
			return HttpResponse("", content_type="application/json", status=404)
		else:
			modes = [mo.type for mo in Mode.objects.all() if mo.event.id == event.id]
			response_data = response("Event init", [0, 0, 255], True, modes)
		return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
	return HttpResponse("", content_type="application/json", status=404)

@csrf_exempt
def scan_post_management(request):

	#	POST management
	if request.method == 'POST':
		res = request.body
		d = json.loads(res)
		scan = Scan(uid = d['id'], mode = d['mode'])

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
			response_data = response("No current event.", [255, 0, 0], True, "Default")
			scan.save()
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=204)

		scan.event = event

		#	Undefined behavior if the mode is invalid.
	
		#	Check if scan amount is reached for current mode and uid.
		all_scans = Scan.objects.filter(mode = scan.mode, uid = scan.uid, event = scan.event)
		current_mode = Mode.objects.filter(event=event, type=scan.mode)	

		if len(all_scans) >= current_mode[0].amount:
			response_data = response("Scan capacity reached.", [255, 0, 0], True, "Default")
			scan.save()
			return HttpResponse(json.dumps(response_data), content_type="application/json", status=205)

		#	Else check if uid assigned to StudentBadge
		else :
			scan.validity = True
			student_badge = StudentBadge.objects.filter(badge__uid = scan.uid)
			if login == "UNDEFINED":
				response_data = response("Badge is not linked to an user", [0, 0, 255], True, "Default")
			else:
				response_data = response("Scan ok", [0, 255, 0], True, "Default")

				#	Modify response message if specific login (Please do not remove this line!)
				response_data = specific_response(response_data, login)

		scan.save()
		return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
	else:
		return scan_page(request)
