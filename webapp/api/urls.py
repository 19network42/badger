from django.urls import path
from api.views import api

app_name = 'api'

urlpatterns = [
    path('api/', api, name = 'api')
]
