import re
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def api(request):
	return HttpResponse("test")