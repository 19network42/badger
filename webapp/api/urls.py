from django.urls import path
from .views import scan, init_page

app_name = 'api'

urlpatterns = [
	path('scan/', scan, name = 'scan'),
	path('init/', init_page),
]