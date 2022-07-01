from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from events.models import Event, Mode
from api.models import Scan
from events.forms import EventForm, ModeForm

#---------------------------------------#
#										#
#				EVENTS					#
#										#
#---------------------------------------#

@csrf_exempt
@login_required(login_url='accounts:login')
def events_page(request):
	context = {
		'events': Event.objects.all(),
	}
	return render(request, "events/events.html", context)


@csrf_exempt
@login_required(login_url='accounts:login')
def	one_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	context = {
		'scans' : [sca for sca in Scan.objects.all() if event.date < sca.date < event.end ],
		'modes' : [mo for mo in Mode.objects.all() if mo.event.id == event_id],
		'event' : event,
	}
	return render(request, "events/one_event.html", context)


@login_required(login_url='accounts:login')
def	update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	event_form = EventForm(request.POST or None, instance=event)

	if request.method == "POST":
		submit = request.POST.get("submit")		
		if submit == "submitted":
			event_form.save()
			return redirect('events:events')
	
	context = {
	'event': event,
	'event_form': event_form,
	}
	mode_page(request, event, context)

	return render(request, "events/update_event.html", context)


@login_required(login_url='accounts:login')
def	add_event(request):
	form = EventForm(request.POST or None)

	if request.method == "POST":
		form.save()
		return HttpResponseRedirect('/update_event/' + str(form.instance.id))

	context = {
		'form': form,
	}
	return render(request, "events/add_event.html", context)


@login_required(login_url='accounts:login')
def	delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.method == "POST":
		event.delete()
		return redirect('events:events')
	context = {'event': event}
	return render(request, "events/delete_event.html", context)


def mode_page(request, event, context):
	mode_form = ModeForm(request.POST or None)
	error = ""
	mode_form.instance.event = event

	if request.method == "POST":
		action = request.POST.get("action")
		delete = request.POST.get("delete")

		#	Add mode
		if action == "add":
			mode_form.save()

			#	Error management
			if mode_form.instance.type in [mo.type for mo in Mode.objects.filter(event=event) if mo != mode_form.instance]:
				error = "Already exist"
				mode_form.instance.delete()
			elif mode_form.instance.type == None or mode_form.instance.amount == None:
				error = "Fill out mode field"
				mode_form.instance.delete()
			elif mode_form.instance.amount <= 0:
				error = "Incorrect amount"
				mode_form.instance.delete()
		
		#	Delete mode
		if delete:
			Mode.objects.filter(id=delete).delete()

	context['modes'] = [mo for mo in Mode.objects.all() if mo.event == event]
	context['mode_form'] = mode_form
	context['mode_error'] = error
	return render(request, 'events/delete_event.html', {'event': event})