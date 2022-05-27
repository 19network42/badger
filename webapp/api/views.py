from asyncio import events
from django.shortcuts import render
from django.http import HttpResponse
from pages.models import Event, get_current_event
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Scan


import json

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


@login_required(login_url='accounts:login')
@csrf_exempt
def scan_page(request, *args, **kwargs):
	#Scan.objects.all().delete()
	if request.method == 'POST':
		res = request.body
		d = json.loads(res)
		scan = Scan(uid = d['id'])
		scan.save()
		response_data = {}
		response_data['result'] = True
		response_data['led'] = True
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	context = {
		'scans': Scan.objects.all()
	}
	return render(request, "scans.html", context)

def scan_history(request, *args, **kwargs):
	context = {
		'scans': Scan.objects.all()
	}
	return render(request, "scan.html", context)
