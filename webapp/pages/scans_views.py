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

@login_required(login_url='pages:login')
def	delete_scan(request, scan_id):
	scan = Scan.objects.get(pk=scan_id)
	if request.method == "POST":
		scan.delete()
		return redirect('scan_page')
	return render(request, 'delete_event.html', {'scan': scan})
