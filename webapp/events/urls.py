from django.urls import path

from events.views import (
							events_page,
							one_event,
							update_event,
							add_event,
							delete_event
						)

app_name = 'events'

urlpatterns = [

	path('events/', events_page, name = 'events'),
	path('events/<int:event_id>/', one_event, name = 'one_event'),
	path('update_event/<int:event_id>/', update_event, name = 'update_event'),
	path('add_event/', add_event, name = 'add_event'),
	path('delete_event/<int:event_id>/', delete_event, name = 'delete_event'),
	
]