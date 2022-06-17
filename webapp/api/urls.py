from django.urls import path
from .views import scan_page, log


urlpatterns = [
	path('scan/', scan_page),
]