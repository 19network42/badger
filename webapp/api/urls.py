from django.urls import path
from .views import scan_page, delete_scan

app_name = 'api'

urlpatterns = [
	#path('', api, name = 'api'),
	#path('scans', api, name = 'api'),
	path('scan/', scan_page, name = 'scan'),
	path('delete_scan/<int:scan_id>/', delete_scan, name = 'delete_scan'),
]
