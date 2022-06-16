from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from events.models import Event
from badges.models import StudentBadge
from django.db.models import Q

#---------------------------------------#
#										#
#				GENERAL					#
#										#
#---------------------------------------#

@csrf_exempt
def	home_page(request, *args, **kwargs):
	return render(request, "home.html")


@login_required(login_url='accounts:login')
@csrf_exempt
def	search_general(request):
	if request.method == "POST":
		searched = request.POST['searched']
		events = Event.objects.filter(name__contains=searched)
		student_bgs = StudentBadge.objects.filter(Q(student__login__contains=searched) | Q(student__displayname__contains=searched))
		return render(request, 'search_general.html', 
			{'searched': searched, 'events': events, 'student_bgs': student_bgs})

