from django.urls import path
from .views import scan_page, delete_scan, init_page, search_scan_page

app_name = 'api'

urlpatterns = [
	#path('', api, name = 'api'),
	#path('scans', api, name = 'api'),
	path('scan/', scan_page, name = 'scan'),
	path('init/', init_page, name = 'init'),
	path('search_scan/', search_scan_page, name='search_scan'),
	path('delete_scan/<int:scan_id>/', delete_scan, name = 'delete_scan'),
]
