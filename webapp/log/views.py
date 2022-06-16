from django.shortcuts import render, redirect
from .consumers import ScanConsumer
from .models import Log
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def index(request):
	log = Log.objects.all()
	return render(request, 'real_time_scan.html')

def test_scan(request):
	channel_layer = get_channel_layer()
	blabla = async_to_sync(channel_layer.group_send)(
		"log",
		{
			"type" : "send.scan",
			"UID" : "blabla",
			"Timestamp" : "9/06/22 , 11h30",
		})
	print('test', dir(blabla))
	return render(request, "add_event.html")