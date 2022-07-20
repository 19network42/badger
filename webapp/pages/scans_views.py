from events.models import Event, get_current_event, Mode
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.http import HttpResponse
from api.models import Scan

@csrf_exempt
def	scan_page(request):
	#	GET management
	context = {
		'scans': Scan.objects.all(),
		'current_scan': Scan.objects.last()
	}
	return render(request, "scans.html", context)

@csrf_exempt
def init_page(request, *args, **kwargs):
	if request.method == 'POST':
		event = get_current_event()
		if not (event):
			return HttpResponse("", content_type="application/json", status=404)
		else:
			modes = [mo.type for mo in Mode.objects.all() if mo.event.id == event.id]
			response_data = response("Event init", [0, 0, 255], True, modes)
		return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
	return HttpResponse("", content_type="application/json", status=404)


def search_scan_page(request):
	if request.method == 'GET':
		return render(request, "search_scans.html", {})

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