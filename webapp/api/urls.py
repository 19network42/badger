from django.urls import path
from .views import scan_page, init_page

app_name = 'api'

urlpatterns = [
	path('scan/', scan_page),
	path('init/', init_page),
]