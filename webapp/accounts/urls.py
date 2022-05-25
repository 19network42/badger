from django.urls import path
from accounts.views import login, authenticate, authorize, logout
from pages.urls import home_page

app_name = 'accounts'

urlpatterns = [
	path('login/', login, name="login"),
	path('authenticate/', authenticate, name='authenticate'),
	path('authorize/', authorize, name='authorize'),
	path('logout/', logout, name='logout'),
]
