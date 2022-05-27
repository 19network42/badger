from django.contrib import admin
from django.urls import path

from pages.views import (
							home_page,
							events_page,
							user_page,
							one_event,
							search_general,
							calendar_page,
							update_event,
							add_event,
							update_mode,
							delete_event
						)

app_name = 'pages'

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', home_page, name = 'home'),
	path('user/', user_page, name = 'user'),
	path('events/', events_page, name = 'events'),
	path('events/<int:event_id>/', one_event, name = 'one_event'),
	path('search_general/', search_general, name = 'search_general'),
	path('calendar/', calendar_page, name = 'calendar'),
	path('update_event/<int:event_id>/', update_event, name = 'update_event'),
	path('add_event/', add_event, name = 'add_event'),
	path('update_mode/<int:event_id>/', update_mode, name = 'update_mode'),
	path('delete_event/<int:event_id>/', delete_event, name = 'delete_event'),
]
