from django.contrib import admin
from django.urls import path

						
from general.views import (
							home_page,
							search_general,
							delete_scan,
							search_scan_page,
							CalendarView
						)


app_name = 'general'

urlpatterns = [

	#	General
	path('', home_page, name = 'home'),
	path('search_general/', search_general, name = 'search_general'),

	#	API
	path('search_scan/', search_scan_page, name='search_scan'),
	path('delete_scan/<int:scan_id>/', delete_scan, name = 'delete_scan'),

	#	Calendar
	path('calendar/', CalendarView.as_view(), name = 'calendar'),
]
