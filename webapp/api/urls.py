from django.urls import path
from .views import (scan_post_management, init_page)

urlpatterns = [
	path('scan/', scan_post_management),
	path('init/', init_page),
]