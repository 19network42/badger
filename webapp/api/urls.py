from django.urls import path
from .views import scan_post_management

urlpatterns = [
	path('scan/', scan_post_management),
]