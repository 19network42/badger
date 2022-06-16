from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'log'

urlpatterns = [
    path('',index),
	path('test/', test_scan)
	
]

# admin.site.site_heard = "Badger Administration"
# admin.site.site_title = "YO"
# admin.site.index_title = "What are you doing here?"