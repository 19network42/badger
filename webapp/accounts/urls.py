from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('authorize/', views.authorize, name='authorize'),
    path('logout/', views.logout, name='logout'),
]
