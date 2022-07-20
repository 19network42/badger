from django.urls import path
<<<<<<< HEAD
from .views import scan_page, log


urlpatterns = [
	path('scan/', scan_page),
=======
from .views import scan, init_page

app_name = 'api'

urlpatterns = [
	path('scan/', scan, name = 'scan'),
	path('init/', init_page),
>>>>>>> 76dac626e5a2e1ba879afb234dd3789c5f8b3a3a
]