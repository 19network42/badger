from django.contrib import admin
from django.urls import path

from pages.views import home_page, scan_page, events_page, user_page, one_event, search_general, calendar_page

app_name = 'pages'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name = 'home'),
    path('user/', user_page, name = 'user'),
    path('scan/', scan_page, name = 'scan'),
    path('events/', events_page, name = 'events'),
    path('events/<int:event_id>/', one_event, name = 'one_event'),
    path('search_general/', search_general, name = 'search_general'),
    path('calendar/', calendar_page, name = 'calendar'),
]

# admin.site.site_heard = "Badger Administration"
# admin.site.site_title = "YO"
# admin.site.index_title = "What are you doing here?"