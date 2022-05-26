from django.urls import path
from .views import scan_page

app_name = 'api'

urlpatterns = [
    #path('', api, name = 'api'),
    #path('scans', api, name = 'api'),
    path('scan/', scan_page, name = 'scan'),
]
