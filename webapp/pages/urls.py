from django.contrib import admin
from django.urls import path
import log
# from badger.webapp.pages.views import CalendarView

from pages.admin_views import (
							user_page,
						)
						
from pages.general_views import (
							home_page,
							search_general,
						)

from api.views import scan_page

from pages.scans_views import (
							delete_scan,
							search_scan_page
						)

from pages.badges_views import (
							add_student,
							update_student,
							testing_student,
							one_student,
							list_student,
							update_studentbadge,
						)

from pages.events_views import (
							events_page,
							one_event,
							update_event,
							add_event,
							delete_event
						)

from pages.admin_views import (
 							login,
							authenticate,
							authorize,
							logout
						)

from pages.calendar_views import (CalendarView)


app_name = 'pages'

urlpatterns = [

	#	General
	path('', home_page, name = 'home'),
	path('search_general/', search_general, name = 'search_general'),

	#	Admin
	path('login/', login, name="login"),
	path('authenticate/', authenticate, name='authenticate'),
	path('authorize/', authorize, name='authorize'),
	path('logout/', logout, name='logout'),
	path('admin/', admin.site.urls),
	path('user/', user_page, name = 'user'),

	#	API
	path('scan/', scan_page, name = 'scan'),
	# path('scan_display/', scan_page, name = 'scan_display'),

	path('search_scan/', search_scan_page, name='search_scan'),
	path('delete_scan/<int:scan_id>/', delete_scan, name = 'delete_scan'),

	#	Badges
	path('add_student/', add_student, name = 'add_student'),
	path('update_student/<int:student_id>/', update_student, name = 'update_student'),
	path('test_student/', testing_student, name = 'test_student'),
	path('students/<int:student_id>/', one_student, name = 'one_student'),
	path('students/', list_student, name = 'students'),
	path('update_studentbadge/<int:scan_id>/', update_studentbadge, name = 'update_studentbadge'),
	
	#	Events
	path('events/', events_page, name = 'events'),
	path('events/<int:event_id>/', one_event, name = 'one_event'),
	path('update_event/<int:event_id>/', update_event, name = 'update_event'),
	path('add_event/', add_event, name = 'add_event'),
	path('delete_event/<int:event_id>/', delete_event, name = 'delete_event'),
	
	#	Calendar
	path('calendar/', CalendarView.as_view(), name = 'calendar'),
]
