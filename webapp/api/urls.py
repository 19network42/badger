from django.contrib import admin
from django.urls import path, include
from .views import scan_post_management

urlpatterns = [
	path('scan/', scan_post_management),
]